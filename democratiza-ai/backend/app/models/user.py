"""
User model - LGPD compliant
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .database import Base


class User(Base):
    """
    User model with LGPD compliance
    Per spec: Authentication, subscription management, audit trail
    """
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    
    # Subscription management
    subscription_tier = Column(String, default="free")  # free, basic, premium
    subscription_expires_at = Column(DateTime, nullable=True)
    
    # LGPD Compliance (Lei Geral de Proteção de Dados)
    consent_terms = Column(Boolean, default=False, nullable=False)
    consent_date = Column(DateTime)
    data_processing_consent = Column(Boolean, default=False)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime)
    
    # Audit fields
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Relationships
    contracts = relationship("Contract", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email}>"
