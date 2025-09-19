from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
from uuid import uuid4

from app.db.database import get_db
from app.db.models import PaymentTransaction, User
from app.api.v1.auth import get_current_user
from app.core.config import settings

router = APIRouter()

# Pydantic models
class PaymentCreate(BaseModel):
    subscription_type: str  # "basic", "premium"
    subscription_months: int
    payment_method: str  # "credit_card", "pix", "boleto"

class PaymentResponse(BaseModel):
    id: str
    amount: float
    status: str
    payment_url: Optional[str] = None
    qr_code: Optional[str] = None
    barcode: Optional[str] = None

class SubscriptionResponse(BaseModel):
    subscription_type: str
    expires_at: Optional[datetime]
    is_active: bool
    days_remaining: Optional[int]

# Subscription pricing (in BRL)
SUBSCRIPTION_PRICES = {
    "basic": {
        1: 29.90,
        3: 79.90,
        6: 149.90,
        12: 279.90
    },
    "premium": {
        1: 49.90,
        3: 129.90,
        6: 239.90,
        12: 449.90
    }
}

class MercadoPagoClient:
    """Client for Mercado Pago API integration"""
    
    def __init__(self):
        self.access_token = settings.MERCADO_PAGO_ACCESS_TOKEN
        self.base_url = "https://api.mercadopago.com"
    
    async def create_preference(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create payment preference in Mercado Pago"""
        
        url = f"{self.base_url}/checkout/preferences"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        preference_data = {
            "items": [
                {
                    "title": payment_data["title"],
                    "description": payment_data["description"],
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": payment_data["amount"]
                }
            ],
            "payer": {
                "email": payment_data["payer_email"],
                "name": payment_data["payer_name"]
            },
            "external_reference": payment_data["external_reference"],
            "notification_url": f"{settings.API_V1_STR}/payments/webhook",
            "back_urls": {
                "success": f"{settings.FRONTEND_URL}/payment/success",
                "failure": f"{settings.FRONTEND_URL}/payment/failure",
                "pending": f"{settings.FRONTEND_URL}/payment/pending"
            },
            "auto_return": "approved",
            "payment_methods": {
                "excluded_payment_types": [],
                "installments": 12 if payment_data["amount"] > 100 else 6
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=preference_data, headers=headers)
            
            if response.status_code == 201:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create payment preference"
                )
    
    async def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """Get payment details from Mercado Pago"""
        
        url = f"{self.base_url}/v1/payments/{payment_id}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Payment not found"
                )

mercado_pago = MercadoPagoClient()

def calculate_subscription_price(subscription_type: str, months: int) -> float:
    """Calculate subscription price"""
    
    if subscription_type not in SUBSCRIPTION_PRICES:
        raise ValueError("Invalid subscription type")
    
    if months not in SUBSCRIPTION_PRICES[subscription_type]:
        raise ValueError("Invalid subscription duration")
    
    return SUBSCRIPTION_PRICES[subscription_type][months]

@router.post("/create", response_model=PaymentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create payment for subscription"""
    
    # Validate subscription type and duration
    if payment_data.subscription_type not in ["basic", "premium"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subscription type"
        )
    
    if payment_data.subscription_months not in [1, 3, 6, 12]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subscription duration"
        )
    
    # Calculate amount
    amount = calculate_subscription_price(
        payment_data.subscription_type,
        payment_data.subscription_months
    )
    
    # Create payment transaction record
    transaction = PaymentTransaction(
        user_id=current_user.id,
        external_id=str(uuid4()),
        amount=amount,
        status="pending",
        payment_method=payment_data.payment_method,
        subscription_type=payment_data.subscription_type,
        subscription_months=payment_data.subscription_months
    )
    
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    
    try:
        # Create Mercado Pago preference
        mp_payment_data = {
            "title": f"Contrato Seguro - {payment_data.subscription_type.title()}",
            "description": f"Assinatura {payment_data.subscription_type} por {payment_data.subscription_months} meses",
            "amount": amount,
            "payer_email": current_user.email,
            "payer_name": current_user.full_name,
            "external_reference": str(transaction.id)
        }
        
        preference = await mercado_pago.create_preference(mp_payment_data)
        
        # Update transaction with external ID
        transaction.external_id = preference["id"]
        transaction.payment_details = {
            "preference_id": preference["id"],
            "init_point": preference["init_point"]
        }
        await db.commit()
        
        return PaymentResponse(
            id=str(transaction.id),
            amount=amount,
            status="pending",
            payment_url=preference["init_point"]
        )
        
    except Exception as e:
        # Update transaction status to failed
        transaction.status = "failed"
        await db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create payment"
        )

@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription_status(
    current_user: User = Depends(get_current_user)
):
    """Get current user subscription status"""
    
    is_active = False
    days_remaining = None
    
    if current_user.subscription_expires_at:
        now = datetime.utcnow()
        if current_user.subscription_expires_at > now:
            is_active = True
            days_remaining = (current_user.subscription_expires_at - now).days
    
    return SubscriptionResponse(
        subscription_type=current_user.subscription_type,
        expires_at=current_user.subscription_expires_at,
        is_active=is_active,
        days_remaining=days_remaining
    )

@router.post("/webhook")
async def payment_webhook(
    payment_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
):
    """Handle Mercado Pago payment webhook"""
    
    try:
        # Validate webhook data
        if "data" not in payment_data or "id" not in payment_data["data"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook data"
            )
        
        payment_id = payment_data["data"]["id"]
        
        # Get payment details from Mercado Pago
        payment_details = await mercado_pago.get_payment(payment_id)
        
        # Find transaction by external reference
        external_reference = payment_details.get("external_reference")
        if not external_reference:
            return {"message": "No external reference found"}
        
        result = await db.execute(
            select(PaymentTransaction).where(PaymentTransaction.id == external_reference)
        )
        transaction = result.scalar_one_or_none()
        
        if not transaction:
            return {"message": "Transaction not found"}
        
        # Update transaction status
        mp_status = payment_details.get("status")
        if mp_status == "approved":
            transaction.status = "paid"
            
            # Update user subscription
            user_result = await db.execute(
                select(User).where(User.id == transaction.user_id)
            )
            user = user_result.scalar_one_or_none()
            
            if user:
                # Calculate new expiration date
                if user.subscription_expires_at and user.subscription_expires_at > datetime.utcnow():
                    # Extend current subscription
                    new_expiration = user.subscription_expires_at + timedelta(days=30 * transaction.subscription_months)
                else:
                    # Start new subscription
                    new_expiration = datetime.utcnow() + timedelta(days=30 * transaction.subscription_months)
                
                user.subscription_type = transaction.subscription_type
                user.subscription_expires_at = new_expiration
        
        elif mp_status in ["rejected", "cancelled"]:
            transaction.status = "failed"
        
        elif mp_status == "pending":
            transaction.status = "pending"
        
        # Update payment details
        transaction.payment_details = payment_details
        
        await db.commit()
        
        return {"message": "Webhook processed successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process webhook"
        )

@router.get("/pricing")
async def get_pricing():
    """Get subscription pricing"""
    return {
        "pricing": SUBSCRIPTION_PRICES,
        "currency": "BRL",
        "features": {
            "basic": [
                "Análise de até 10 contratos por mês",
                "Chat com IA especializada",
                "Relatórios de risco básicos",
                "Suporte por email"
            ],
            "premium": [
                "Análise ilimitada de contratos",
                "Chat com IA especializada",
                "Relatórios detalhados de risco",
                "Assinatura eletrônica D4Sign",
                "Suporte prioritário",
                "Histórico completo"
            ]
        }
    }
