"""
Subscription and Payment Models for Democratiza AI
"""
from sqlalchemy import Column, Integer, String, Decimal, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.db.models import Base
from datetime import datetime, timedelta
import uuid

class Plan(Base):
    """Payment plans for the platform"""
    __tablename__ = "plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)  # "Avulso", "Básico", "Premium", "Empresarial"
    type = Column(String(20), nullable=False)   # "pay_per_use", "monthly", "annual"
    price = Column(Decimal(10, 2), nullable=False)
    analyses_included = Column(Integer, nullable=True)  # null = unlimited
    features = Column(JSON, nullable=True)  # JSON with feature list
    is_active = Column(Boolean, default=True)
    mercado_pago_plan_id = Column(String(100), nullable=True)  # For subscriptions
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscriptions = relationship("UserSubscription", back_populates="plan")
    transactions = relationship("Transaction", back_populates="plan")

class UserSubscription(Base):
    """User subscription management"""
    __tablename__ = "user_subscriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=False)
    
    # Subscription status and limits
    status = Column(String(20), nullable=False, default="pending")  # "pending", "active", "cancelled", "expired"
    analyses_remaining = Column(Integer, nullable=True)  # null = unlimited
    analyses_used = Column(Integer, default=0)
    
    # Dates
    starts_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    
    # External references
    mercado_pago_subscription_id = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    
    def has_remaining_analyses(self) -> bool:
        """Check if user has remaining analyses"""
        if self.analyses_remaining is None:  # Unlimited
            return True
        return self.analyses_remaining > 0
    
    def consume_analysis(self) -> bool:
        """Consume one analysis credit"""
        if not self.has_remaining_analyses():
            return False
            
        if self.analyses_remaining is not None:
            self.analyses_remaining -= 1
        
        self.analyses_used += 1
        return True

class Transaction(Base):
    """Payment transactions"""
    __tablename__ = "transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan_id = Column(UUID(as_uuid=True), ForeignKey("plans.id"), nullable=True)
    
    # Transaction details
    amount = Column(Decimal(10, 2), nullable=False)
    type = Column(String(20), nullable=False)  # "subscription", "pay_per_use"
    status = Column(String(20), nullable=False, default="pending")  # "pending", "approved", "cancelled", "refunded"
    description = Column(String(255), nullable=True)
    
    # External references
    mercado_pago_payment_id = Column(String(100), nullable=True)
    external_reference = Column(String(100), nullable=True)
    
    # Payment details
    payment_method = Column(String(50), nullable=True)  # "pix", "credit_card", etc.
    approved_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    plan = relationship("Plan", back_populates="transactions")

class SignatureRequest(Base):
    """Electronic signature requests"""
    __tablename__ = "signature_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=True)
    
    # Document details
    document_name = Column(String(255), nullable=False)
    original_file_url = Column(String(500), nullable=False)
    signed_file_url = Column(String(500), nullable=True)
    
    # D4Sign integration
    d4sign_document_uuid = Column(String(100), nullable=False, unique=True)
    d4sign_folder_uuid = Column(String(100), nullable=True)
    
    # Status tracking
    status = Column(String(20), nullable=False, default="sent")  # "sent", "signed", "cancelled", "expired"
    signers_count = Column(Integer, default=0)
    signers_completed = Column(Integer, default=0)
    
    # Dates
    sent_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)  # Auto-expire after X days
    
    # Additional data
    signers_data = Column(JSON, nullable=False)  # List of signers info
    webhook_events = Column(JSON, nullable=True)  # D4Sign webhook history
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="signature_requests")
    contract = relationship("Contract", back_populates="signature_requests")
    signers = relationship("Signer", back_populates="signature_request")
    
    @property
    def is_completed(self) -> bool:
        """Check if all signers have signed"""
        return self.signers_completed >= self.signers_count
    
    @property
    def progress_percentage(self) -> float:
        """Get completion percentage"""
        if self.signers_count == 0:
            return 0.0
        return (self.signers_completed / self.signers_count) * 100

class Signer(Base):
    """Individual signers for signature requests"""
    __tablename__ = "signers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signature_request_id = Column(UUID(as_uuid=True), ForeignKey("signature_requests.id"), nullable=False)
    
    # Signer details
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    document = Column(String(20), nullable=True)  # CPF/CNPJ
    phone = Column(String(20), nullable=True)
    
    # Signature status
    signed = Column(Boolean, default=False)
    signed_at = Column(DateTime, nullable=True)
    signature_ip = Column(String(45), nullable=True)  # IP address when signed
    
    # D4Sign specific
    d4sign_signer_uuid = Column(String(100), nullable=True)
    signature_url = Column(String(500), nullable=True)  # Direct signature link
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    signature_request = relationship("SignatureRequest", back_populates="signers")