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
    subscriptions = relationship("UserSubscription", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    signature_requests = relationship("SignatureRequest", back_populates="user")

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
    signature_requests = relationship("SignatureRequest", back_populates="contract")
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
    message_metadata = Column(JSON)  # For storing additional context
    
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

class LegalDocument(Base):
    __tablename__ = "legal_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Document metadata
    title = Column(String, nullable=False)
    document_type = Column(String, nullable=False)  # lei, decreto, jurisprudencia, doutrina, etc.
    category = Column(String, nullable=False)  # locacao, telecom, financeiro, geral
    subcategory = Column(String)
    
    # Content
    content = Column(Text, nullable=False)
    summary = Column(Text)
    abstract = Column(Text)  # For jurisprudence cases
    
    # Source information
    source = Column(String, nullable=False)  # STF, STJ, TJ-SP, etc.
    source_url = Column(String)
    reference_number = Column(String)  # Process number, law number, etc.
    publication_date = Column(DateTime(timezone=True))
    
    # Legal metadata
    court = Column(String)  # For jurisprudence
    judge = Column(String)  # For jurisprudence
    legal_area = Column(JSON)  # Array of legal areas
    keywords = Column(JSON)  # Array of keywords
    
    # Processing status
    processing_status = Column(String, default="pending")  # pending, processing, indexed, failed
    chunk_count = Column(Integer, default=0)
    
    # Quality metrics
    relevance_score = Column(Float, default=1.0)
    authority_level = Column(String, default="medium")  # high, medium, low
    
    # Metadata
    is_active = Column(Boolean, default=True)
    indexed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    chunks = relationship("LegalChunk", back_populates="document", cascade="all, delete-orphan")

class LegalChunk(Base):
    __tablename__ = "legal_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("legal_documents.id"), nullable=False)
    
    # Chunk content and metadata
    content = Column(Text, nullable=False)
    chunk_type = Column(String, default="text")  # text, article, paragraph, summary
    chunk_order = Column(Integer, nullable=False)
    
    # Position in document
    start_position = Column(Integer)
    end_position = Column(Integer)
    page_number = Column(Integer)
    section_title = Column(String)
    
    # Vector embedding
    embedding = Column(Vector(1536))  # OpenAI embeddings dimension
    
    # Content analysis
    word_count = Column(Integer)
    char_count = Column(Integer)
    importance_score = Column(Float, default=1.0)
    
    # Legal context
    legal_concepts = Column(JSON)  # Array of identified legal concepts
    entities = Column(JSON)  # Named entities (laws, articles, etc.)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    document = relationship("LegalDocument", back_populates="chunks")

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
    audit_metadata = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")


class StorageAuditLog(Base):
    __tablename__ = "storage_audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Operation details
    operation = Column(String, nullable=False)  # upload, download, delete, presigned_url
    file_id = Column(String, nullable=False)
    file_name = Column(String)
    file_size = Column(Integer)
    
    # Request details
    ip_address = Column(String)
    user_agent = Column(String)
    
    # Result
    success = Column(Boolean, nullable=False)
    error_message = Column(Text)
    
    # Metadata (using different name to avoid SQLAlchemy conflicts)
    operation_metadata = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
