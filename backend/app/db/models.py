from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Subscription info
    subscription_type = Column(String, default="free")  # free, basic, premium
    subscription_expires_at = Column(DateTime(timezone=True))
    
    # Relationships
    contracts = relationship("Contract", back_populates="owner")
    chat_sessions = relationship("ChatSession", back_populates="user")

class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Contract metadata
    title = Column(String, nullable=False)
    contract_type = Column(String, nullable=False)  # locacao, telecom, financeiro, etc.
    original_filename = Column(String)
    file_url = Column(String)  # Cloudflare R2 URL
    file_size = Column(Integer)
    mime_type = Column(String)
    
    # OCR and processing
    extracted_text = Column(Text)
    ocr_confidence = Column(Float)
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    
    # Analysis results
    risk_level = Column(String)  # Alto Risco, Médio Risco, Baixo Risco
    analysis_summary = Column(Text)
    analysis_results = Column(JSON)  # Full analysis from agents
    confidence_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    analyzed_at = Column(DateTime(timezone=True))
    
    # Relationships
    owner = relationship("User", back_populates="contracts")
    chat_sessions = relationship("ChatSession", back_populates="contract")
    risk_factors = relationship("RiskFactor", back_populates="contract")

class RiskFactor(Base):
    __tablename__ = "risk_factors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False)
    
    # Risk details
    risk_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String, nullable=False)  # high, medium, low
    clause_text = Column(Text)
    recommendation = Column(Text)
    legal_basis = Column(String)
    
    # Position in document
    page_number = Column(Integer)
    clause_number = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    contract = relationship("Contract", back_populates="risk_factors")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=True)
    
    # Session metadata
    title = Column(String, default="Nova Conversa")
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    contract = relationship("Contract", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    
    # Message content
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    message_type = Column(String, default="text")  # text, image, file
    
    # Additional metadata
    metadata = Column(JSON)  # For storing additional context
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Content
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    
    # Categorization
    category = Column(String, nullable=False)  # locacao, telecom, financeiro, geral
    subcategory = Column(String)
    tags = Column(JSON)  # Array of tags
    
    # Source information
    source = Column(String)  # lei, jurisprudencia, doutrina, etc.
    source_url = Column(String)
    confidence_level = Column(Float, default=1.0)
    
    # Vector embedding for RAG
    embedding = Column(Vector(1536))  # OpenAI embeddings dimension
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Transaction details
    external_id = Column(String, unique=True)  # Mercado Pago transaction ID
    amount = Column(Float, nullable=False)
    currency = Column(String, default="BRL")
    status = Column(String, nullable=False)  # pending, paid, failed, refunded
    
    # Payment method
    payment_method = Column(String)  # credit_card, pix, boleto
    payment_details = Column(JSON)
    
    # Subscription related
    subscription_type = Column(String)  # basic, premium
    subscription_months = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Action details
    action = Column(String, nullable=False)  # upload, analyze, chat, etc.
    resource_type = Column(String)  # contract, user, etc.
    resource_id = Column(String)
    
    # Request details
    ip_address = Column(String)
    user_agent = Column(String)
    metadata = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
