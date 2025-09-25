""""""

Payments API endpointsPayments API endpoints

""""""

from typing import List, Dict, Anyfrom typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Requestfrom fastapi import APIRouter, Depends, HTTPException, Request

from sqlalchemy.orm import Sessionfrom sqlalchemy.orm import Session

from pydantic import BaseModelfrom pydantic import BaseModel

from app.db.database import get_dbfrom app.db.database import get_db

from app.services.payment_service import PaymentServicefrom app.services.payment_service import PaymentService

from app.api.v1.auth import get_current_userfrom app.api.v1.auth import get_current_user

from app.db.models import Userfrom app.db.models import User



router = APIRouter()router = APIRouter()



class PayPerUseRequest(BaseModel):class PayPerUseRequest(BaseModel):

    """Request model for pay-per-use analysis"""    """Request model for pay-per-use analysis"""

    analysis_type: str = "standard"  # standard, premium, express    analysis_type: str = "standard"  # standard, premium, express

        

class SubscriptionPaymentRequest(BaseModel):class SubscriptionPaymentRequest(BaseModel):

    """Request model for subscription payment"""    """Request model for subscription payment"""

    plan_id: str    plan_id: str

    

@router.post("/pay-per-use")class WebhookRequest(BaseModel):

async def create_pay_per_use_payment(    """Request model for Mercado Pago webhook"""

    request: PayPerUseRequest,    action: str

    current_user: User = Depends(get_current_user),    api_version: str

    db: Session = Depends(get_db)    data: Dict[str, Any]

):    date_created: str

    """Create a pay-per-use payment for contract analysis"""    id: int

        live_mode: bool

    try:    type: str

        payment_service = PaymentService(db)    user_id: str

        

        result = await payment_service.create_pay_per_use_payment(class MercadoPagoClient:

            user_id=str(current_user.id),    """Client for Mercado Pago API integration"""

            analysis_type=request.analysis_type    

        )    def __init__(self):

                self.access_token = settings.MERCADO_PAGO_ACCESS_TOKEN

        return {        self.base_url = "https://api.mercadopago.com"

            "status": "success",    

            "payment_id": result["payment_id"],    async def create_preference(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:

            "payment_url": result["payment_url"],        """Create payment preference in Mercado Pago"""

            "amount": result["amount"],        

            "analysis_type": request.analysis_type,        url = f"{self.base_url}/checkout/preferences"

            "expires_at": result["expires_at"]        headers = {

        }            "Authorization": f"Bearer {self.access_token}",

                    "Content-Type": "application/json"

    except Exception as e:        }

        raise HTTPException(status_code=400, detail=str(e))        

        preference_data = {

@router.post("/subscription")            "items": [

async def create_subscription_payment(                {

    request: SubscriptionPaymentRequest,                    "title": payment_data["title"],

    current_user: User = Depends(get_current_user),                    "description": payment_data["description"],

    db: Session = Depends(get_db)                    "quantity": 1,

):                    "currency_id": "BRL",

    """Create a subscription payment"""                    "unit_price": payment_data["amount"]

                    }

    try:            ],

        payment_service = PaymentService(db)            "payer": {

                        "email": payment_data["payer_email"],

        result = await payment_service.create_subscription_payment(                "name": payment_data["payer_name"]

            user_id=str(current_user.id),            },

            plan_id=request.plan_id            "external_reference": payment_data["external_reference"],

        )            "notification_url": f"{settings.API_V1_STR}/payments/webhook",

                    "back_urls": {

        return {                "success": f"{settings.FRONTEND_URL}/payment/success",

            "status": "success",                "failure": f"{settings.FRONTEND_URL}/payment/failure",

            "payment_id": result["payment_id"],                "pending": f"{settings.FRONTEND_URL}/payment/pending"

            "payment_url": result["payment_url"],            },

            "amount": result["amount"],            "auto_return": "approved",

            "plan": result["plan"],            "payment_methods": {

            "expires_at": result["expires_at"]                "excluded_payment_types": [],

        }                "installments": 12 if payment_data["amount"] > 100 else 6

                    }

    except Exception as e:        }

        raise HTTPException(status_code=400, detail=str(e))        

        async with httpx.AsyncClient() as client:

@router.get("/plans")            response = await client.post(url, json=preference_data, headers=headers)

async def get_available_plans(            

    db: Session = Depends(get_db)            if response.status_code == 201:

):                return response.json()

    """Get all available subscription plans"""            else:

                    raise HTTPException(

    try:                    status_code=status.HTTP_400_BAD_REQUEST,

        payment_service = PaymentService(db)                    detail="Failed to create payment preference"

        plans = await payment_service.get_available_plans()                )

            

        return {    async def get_payment(self, payment_id: str) -> Dict[str, Any]:

            "status": "success",        """Get payment details from Mercado Pago"""

            "plans": plans        

        }        url = f"{self.base_url}/v1/payments/{payment_id}"

                headers = {

    except Exception as e:            "Authorization": f"Bearer {self.access_token}"

        raise HTTPException(status_code=400, detail=str(e))        }

        

@router.get("/user/subscription")        async with httpx.AsyncClient() as client:

async def get_user_subscription(            response = await client.get(url, headers=headers)

    current_user: User = Depends(get_current_user),            

    db: Session = Depends(get_db)            if response.status_code == 200:

):                return response.json()

    """Get current user's subscription status"""            else:

                    raise HTTPException(

    try:                    status_code=status.HTTP_404_NOT_FOUND,

        payment_service = PaymentService(db)                    detail="Payment not found"

        subscription = await payment_service.get_user_subscription(str(current_user.id))                )

        

        return {mercado_pago = MercadoPagoClient()

            "status": "success",

            "subscription": subscriptiondef calculate_subscription_price(subscription_type: str, months: int) -> float:

        }    """Calculate subscription price"""

            

    except Exception as e:    if subscription_type not in SUBSCRIPTION_PRICES:

        raise HTTPException(status_code=400, detail=str(e))        raise ValueError("Invalid subscription type")

    

@router.get("/user/transactions")    if months not in SUBSCRIPTION_PRICES[subscription_type]:

async def get_user_transactions(        raise ValueError("Invalid subscription duration")

    current_user: User = Depends(get_current_user),    

    db: Session = Depends(get_db)    return SUBSCRIPTION_PRICES[subscription_type][months]

):

    """Get user's payment history"""@router.post("/create", response_model=PaymentResponse)

    async def create_payment(

    try:    payment_data: PaymentCreate,

        payment_service = PaymentService(db)    current_user: User = Depends(get_current_user),

        transactions = await payment_service.get_user_transactions(str(current_user.id))    db: AsyncSession = Depends(get_db)

        ):

        return {    """Create payment for subscription"""

            "status": "success",    

            "transactions": transactions    # Validate subscription type and duration

        }    if payment_data.subscription_type not in ["basic", "premium"]:

                raise HTTPException(

    except Exception as e:            status_code=status.HTTP_400_BAD_REQUEST,

        raise HTTPException(status_code=400, detail=str(e))            detail="Invalid subscription type"

        )

@router.get("/user/can-analyze")    

async def check_user_can_analyze(    if payment_data.subscription_months not in [1, 3, 6, 12]:

    current_user: User = Depends(get_current_user),        raise HTTPException(

    db: Session = Depends(get_db)            status_code=status.HTTP_400_BAD_REQUEST,

):            detail="Invalid subscription duration"

    """Check if user can perform contract analysis"""        )

        

    try:    # Calculate amount

        payment_service = PaymentService(db)    amount = calculate_subscription_price(

        result = await payment_service.check_user_can_analyze(str(current_user.id))        payment_data.subscription_type,

                payment_data.subscription_months

        return {    )

            "status": "success",    

            "can_analyze": result["can_analyze"],    # Create payment transaction record

            "reason": result["reason"],    transaction = PaymentTransaction(

            "remaining_analyses": result.get("remaining_analyses"),        user_id=current_user.id,

            "subscription_expires": result.get("subscription_expires")        external_id=str(uuid4()),

        }        amount=amount,

                status="pending",

    except Exception as e:        payment_method=payment_data.payment_method,

        raise HTTPException(status_code=400, detail=str(e))        subscription_type=payment_data.subscription_type,

        subscription_months=payment_data.subscription_months

@router.post("/webhook")    )

async def mercado_pago_webhook(    

    request: Request,    db.add(transaction)

    db: Session = Depends(get_db)    await db.commit()

):    await db.refresh(transaction)

    """Handle Mercado Pago webhook notifications"""    

        try:

    try:        # Create Mercado Pago preference

        # Parse webhook data        mp_payment_data = {

        webhook_data = await request.json()            "title": f"Contrato Seguro - {payment_data.subscription_type.title()}",

                    "description": f"Assinatura {payment_data.subscription_type} por {payment_data.subscription_months} meses",

        payment_service = PaymentService(db)            "amount": amount,

        result = await payment_service.process_webhook(webhook_data)            "payer_email": current_user.email,

                    "payer_name": current_user.full_name,

        return {            "external_reference": str(transaction.id)

            "status": "processed" if result["processed"] else "ignored",        }

            "message": result["message"]        

        }        preference = await mercado_pago.create_preference(mp_payment_data)

                

    except Exception as e:        # Update transaction with external ID

        # Log error but return success to avoid webhook retries        transaction.external_id = preference["id"]

        print(f"Webhook processing error: {str(e)}")        transaction.payment_details = {

        return {"status": "error", "message": "Internal error"}            "preference_id": preference["id"],

            "init_point": preference["init_point"]

@router.post("/consume-analysis")        }

async def consume_analysis_credit(        await db.commit()

    current_user: User = Depends(get_current_user),        

    db: Session = Depends(get_db)        return PaymentResponse(

):            id=str(transaction.id),

    """Consume one analysis credit (called when user performs analysis)"""            amount=amount,

                status="pending",

    try:            payment_url=preference["init_point"]

        payment_service = PaymentService(db)        )

        result = await payment_service.consume_analysis_credit(str(current_user.id))        

            except Exception as e:

        return {        # Update transaction status to failed

            "status": "success",        transaction.status = "failed"

            "consumed": True,        await db.commit()

            "remaining_analyses": result.get("remaining_analyses"),        

            "subscription_expires": result.get("subscription_expires")        raise HTTPException(

        }            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

                    detail="Failed to create payment"

    except Exception as e:        )

        raise HTTPException(status_code=400, detail=str(e))
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
