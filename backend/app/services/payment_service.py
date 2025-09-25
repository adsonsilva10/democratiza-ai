"""
Payment Service for Mercado Pago Integration
"""
import os
import httpx
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.subscription import Plan, UserSubscription, Transaction
from app.db.models import User
from app.core.config import settings

class PaymentService:
    """Service for handling payments via Mercado Pago"""
    
    def __init__(self, db: Session):
        self.db = db
        self.access_token = settings.MERCADO_PAGO_ACCESS_TOKEN
        self.base_url = "https://api.mercadopago.com/v1"
        
    async def get_available_plans(self) -> Dict[str, List[Dict]]:
        """Get all available payment plans"""
        result = await self.db.execute(
            select(Plan).where(Plan.is_active == True)
        )
        plans = result.scalars().all()
        
        pay_per_use = [
            {
                "id": str(plan.id),
                "name": plan.name,
                "price": float(plan.price),
                "analyses": plan.analyses_included,
                "features": plan.features or []
            }
            for plan in plans if plan.type == "pay_per_use"
        ]
        
        subscriptions = [
            {
                "id": str(plan.id),
                "name": plan.name,
                "type": plan.type,
                "price": float(plan.price),
                "analyses": plan.analyses_included,
                "features": plan.features or []
            }
            for plan in plans if plan.type in ["monthly", "annual"]
        ]
        
        return {
            "pay_per_use": pay_per_use,
            "subscriptions": subscriptions
        }
    
    async def create_pay_per_use_payment(
        self, 
        user_id: str, 
        contract_analysis_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a pay-per-use payment for contract analysis"""
        
        # Get the pay-per-use plan
        result = await self.db.execute(
            select(Plan).where(
                Plan.type == "pay_per_use",
                Plan.is_active == True
            )
        )
        plan = result.scalar_one_or_none()
        
        if not plan:
            raise ValueError("Pay-per-use plan not found")
        
        # Get user details
        user_result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise ValueError("User not found")
        
        # Create payment data for Mercado Pago
        payment_data = {
            "transaction_amount": float(plan.price),
            "description": f"Análise de Contrato - {plan.name}",
            "payment_method_id": "pix",
            "payer": {
                "email": user.email,
                "first_name": user.full_name.split()[0] if user.full_name else "Usuario",
                "last_name": " ".join(user.full_name.split()[1:]) if len(user.full_name.split()) > 1 else ""
            },
            "external_reference": f"analysis_{contract_analysis_id}" if contract_analysis_id else f"credit_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "notification_url": f"{settings.API_BASE_URL}/api/v1/payments/webhook",
            "metadata": {
                "user_id": user_id,
                "plan_id": str(plan.id),
                "contract_analysis_id": contract_analysis_id
            }
        }
        
        # Create payment in Mercado Pago
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                f"{self.base_url}/payments",
                json=payment_data,
                headers=headers
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Mercado Pago API error: {response.text}")
            
            payment_response = response.json()
        
        # Save transaction in database
        transaction = Transaction(
            user_id=user_id,
            plan_id=plan.id,
            amount=plan.price,
            type="pay_per_use",
            status="pending",
            description=payment_data["description"],
            mercado_pago_payment_id=str(payment_response["id"]),
            external_reference=payment_data["external_reference"],
            payment_method="pix"
        )
        
        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
        
        return {
            "transaction_id": str(transaction.id),
            "payment_id": payment_response["id"],
            "status": payment_response["status"],
            "qr_code": payment_response["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": payment_response["point_of_interaction"]["transaction_data"]["qr_code_base64"],
            "ticket_url": payment_response["point_of_interaction"]["transaction_data"]["ticket_url"],
            "amount": float(plan.price),
            "expires_at": payment_response.get("date_of_expiration")
        }
    
    async def create_subscription_payment(
        self, 
        user_id: str, 
        plan_id: str
    ) -> Dict[str, Any]:
        """Create a subscription payment"""
        
        # Get plan details
        result = await self.db.execute(
            select(Plan).where(Plan.id == plan_id, Plan.is_active == True)
        )
        plan = result.scalar_one_or_none()
        
        if not plan:
            raise ValueError("Plan not found")
        
        if plan.type == "pay_per_use":
            raise ValueError("Cannot create subscription for pay-per-use plan")
        
        # Get user details
        user_result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise ValueError("User not found")
        
        # Check if user already has active subscription
        existing_sub_result = await self.db.execute(
            select(UserSubscription).where(
                UserSubscription.user_id == user_id,
                UserSubscription.status == "active"
            )
        )
        existing_sub = existing_sub_result.scalar_one_or_none()
        
        if existing_sub:
            raise ValueError("User already has an active subscription")
        
        # Create subscription preference for checkout
        preference_data = {
            "items": [
                {
                    "title": f"Plano {plan.name} - Democratiza AI",
                    "quantity": 1,
                    "unit_price": float(plan.price),
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "name": user.full_name,
                "email": user.email
            },
            "payment_methods": {
                "excluded_payment_types": [],
                "installments": 12 if plan.type == "annual" else 1
            },
            "back_urls": {
                "success": f"{settings.FRONTEND_URL}/dashboard/pagamentos?status=success",
                "failure": f"{settings.FRONTEND_URL}/dashboard/pagamentos?status=failure",
                "pending": f"{settings.FRONTEND_URL}/dashboard/pagamentos?status=pending"
            },
            "auto_return": "approved",
            "external_reference": f"subscription_{user_id}_{plan_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "notification_url": f"{settings.API_BASE_URL}/api/v1/payments/webhook",
            "metadata": {
                "user_id": user_id,
                "plan_id": plan_id,
                "subscription_type": plan.type
            }
        }
        
        # Create preference in Mercado Pago
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = await client.post(
                f"{self.base_url}/checkout/preferences",
                json=preference_data,
                headers=headers
            )
            
            if response.status_code not in [200, 201]:
                raise Exception(f"Mercado Pago API error: {response.text}")
            
            preference_response = response.json()
        
        # Create pending subscription
        subscription = UserSubscription(
            user_id=user_id,
            plan_id=plan_id,
            status="pending",
            analyses_remaining=plan.analyses_included
        )
        
        self.db.add(subscription)
        
        # Create pending transaction
        transaction = Transaction(
            user_id=user_id,
            plan_id=plan_id,
            amount=plan.price,
            type="subscription",
            status="pending",
            description=f"Assinatura {plan.name}",
            external_reference=preference_data["external_reference"]
        )
        
        self.db.add(transaction)
        await self.db.commit()
        
        return {
            "subscription_id": str(subscription.id),
            "preference_id": preference_response["id"],
            "init_point": preference_response["init_point"],
            "sandbox_init_point": preference_response.get("sandbox_init_point"),
            "checkout_url": preference_response["init_point"]
        }
    
    async def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process webhook notifications from Mercado Pago"""
        
        action = webhook_data.get("action")
        data_id = webhook_data.get("data", {}).get("id")
        
        if not data_id:
            return {"status": "ignored", "reason": "No data ID"}
        
        if action == "payment.created" or action == "payment.updated":
            return await self._process_payment_webhook(data_id)
        
        return {"status": "ignored", "reason": f"Unhandled action: {action}"}
    
    async def _process_payment_webhook(self, payment_id: str) -> Dict[str, Any]:
        """Process payment webhook"""
        
        # Get payment details from Mercado Pago
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            
            response = await client.get(
                f"{self.base_url}/payments/{payment_id}",
                headers=headers
            )
            
            if response.status_code != 200:
                return {"status": "error", "reason": "Could not fetch payment"}
            
            payment_data = response.json()
        
        # Find transaction in database
        transaction_result = await self.db.execute(
            select(Transaction).where(
                Transaction.mercado_pago_payment_id == payment_id
            )
        )
        transaction = transaction_result.scalar_one_or_none()
        
        if not transaction:
            return {"status": "ignored", "reason": "Transaction not found"}
        
        # Update transaction status
        old_status = transaction.status
        new_status = self._map_mercado_pago_status(payment_data["status"])
        
        transaction.status = new_status
        transaction.payment_method = payment_data.get("payment_method_id")
        
        if new_status == "approved":
            transaction.approved_at = datetime.utcnow()
            
            # If this is a subscription payment, activate subscription
            if transaction.type == "subscription":
                await self._activate_subscription(transaction.user_id, transaction.plan_id)
            
            # If pay-per-use, add analysis credit
            elif transaction.type == "pay_per_use":
                await self._add_analysis_credit(transaction.user_id)
        
        await self.db.commit()
        
        return {
            "status": "processed",
            "transaction_id": str(transaction.id),
            "old_status": old_status,
            "new_status": new_status
        }
    
    def _map_mercado_pago_status(self, mp_status: str) -> str:
        """Map Mercado Pago status to our internal status"""
        status_mapping = {
            "approved": "approved",
            "pending": "pending", 
            "authorized": "pending",
            "in_process": "pending",
            "in_mediation": "pending",
            "rejected": "cancelled",
            "cancelled": "cancelled",
            "refunded": "refunded",
            "charged_back": "refunded"
        }
        return status_mapping.get(mp_status, "pending")
    
    async def _activate_subscription(self, user_id: str, plan_id: str):
        """Activate user subscription"""
        
        # Get plan details
        plan_result = await self.db.execute(
            select(Plan).where(Plan.id == plan_id)
        )
        plan = plan_result.scalar_one()
        
        # Find pending subscription
        sub_result = await self.db.execute(
            select(UserSubscription).where(
                UserSubscription.user_id == user_id,
                UserSubscription.plan_id == plan_id,
                UserSubscription.status == "pending"
            )
        )
        subscription = sub_result.scalar_one_or_none()
        
        if subscription:
            subscription.status = "active"
            subscription.starts_at = datetime.utcnow()
            
            # Calculate expiration date
            if plan.type == "monthly":
                subscription.expires_at = datetime.utcnow() + timedelta(days=30)
            elif plan.type == "annual":
                subscription.expires_at = datetime.utcnow() + timedelta(days=365)
            
            subscription.analyses_remaining = plan.analyses_included
    
    async def _add_analysis_credit(self, user_id: str):
        """Add analysis credit for pay-per-use payment"""
        # For now, we can create a temporary "credit" subscription
        # or implement a credit system in the User model
        pass
    
    async def check_user_can_analyze(self, user_id: str) -> Dict[str, Any]:
        """Check if user can perform an analysis"""
        
        # Get active subscription
        result = await self.db.execute(
            select(UserSubscription).where(
                UserSubscription.user_id == user_id,
                UserSubscription.status == "active"
            )
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            return {
                "can_analyze": False,
                "reason": "no_active_subscription",
                "message": "Você precisa de um plano ativo para analisar contratos"
            }
        
        # Check if subscription is expired
        if subscription.expires_at and subscription.expires_at < datetime.utcnow():
            subscription.status = "expired"
            await self.db.commit()
            
            return {
                "can_analyze": False,
                "reason": "subscription_expired", 
                "message": "Sua assinatura expirou"
            }
        
        # Check analysis limit
        if not subscription.has_remaining_analyses():
            return {
                "can_analyze": False,
                "reason": "no_analyses_remaining",
                "message": f"Você utilizou todas as {subscription.plan.analyses_included} análises do seu plano",
                "analyses_used": subscription.analyses_used,
                "analyses_limit": subscription.plan.analyses_included
            }
        
        return {
            "can_analyze": True,
            "subscription": {
                "plan_name": subscription.plan.name,
                "analyses_remaining": subscription.analyses_remaining,
                "analyses_used": subscription.analyses_used,
                "expires_at": subscription.expires_at.isoformat() if subscription.expires_at else None
            }
        }
    
    async def consume_analysis_credit(self, user_id: str) -> bool:
        """Consume one analysis credit from user's subscription"""
        
        result = await self.db.execute(
            select(UserSubscription).where(
                UserSubscription.user_id == user_id,
                UserSubscription.status == "active"
            )
        )
        subscription = result.scalar_one_or_none()
        
        if not subscription:
            return False
        
        success = subscription.consume_analysis()
        if success:
            await self.db.commit()
        
        return success