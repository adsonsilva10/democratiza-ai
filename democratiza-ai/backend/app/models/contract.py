"""
Contract model with pg_vector support
"""

from sqlalchemy import Column, String, Text, DateTime, Enum as SQLEnum, ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
import uuid
import enum
from datetime import datetime
from .database import Base


class ContractType(str, enum.Enum):
    """Contract types per spec: Domain specialists"""
    RENTAL = "rental"        # rental_agent.py
    TELECOM = "telecom"      # telecom_agent.py
    FINANCIAL = "financial"  # financial_agent.py
    EMPLOYMENT = "employment"
    SERVICE = "service"
    OTHER = "other"


class RiskLevel(str, enum.Enum):
    """Risk Classification System per spec"""
    HIGH = "high"      # Alto Risco - Red indicators
    MEDIUM = "medium"  # Médio Risco - Yellow indicators
    LOW = "low"        # Baixo Risco - Green indicators
    UNKNOWN = "unknown"


class ContractStatus(str, enum.Enum):
    """Document Processing Flow states per spec"""
    UPLOADED = "uploaded"          # Step 1: Upload → R2
    PROCESSING = "processing"      # Step 2: OCR extraction
    CLASSIFYING = "classifying"    # Step 3: classifier_agent.py
    ANALYZING = "analyzing"        # Step 4: Specialist agent
    ANALYZED = "analyzed"          # Step 5: Complete
    SIGNED = "signed"              # D4Sign integration
    ARCHIVED = "archived"
    ERROR = "error"


class Contract(Base):
    """
    Contract model - Core entity
    Per spec: Encryption at rest, pg_vector extension for RAG
    """
    __tablename__ = "contracts"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Basic info
    title = Column(String, nullable=False)
    contract_type = Column(SQLEnum(ContractType), index=True)
    status = Column(SQLEnum(ContractStatus), default=ContractStatus.UPLOADED, nullable=False, index=True)
    
    # File storage (Cloudflare R2)
    file_url = Column(String, nullable=False)  # r2://bucket/path format
    file_name = Column(String)
    file_size = Column(Integer)
    file_hash = Column(String)  # SHA256 for integrity verification
    
    # OCR extraction (via ocr_service.py)
    extracted_text = Column(Text)
    ocr_confidence = Column(Float)  # 0.0-1.0
    ocr_method = Column(String)  # direct_extraction, google_vision_ocr, etc
    
    # RAG & Vector search (requires pg_vector extension)
    text_embedding = Column(Vector(1536))  # OpenAI ada-002 embeddings (1536 dimensions)
    
    # AI Analysis results (structured JSON per contract_analysis_service.py)
    analysis_result = Column(JSONB)
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.UNKNOWN, index=True)
    risk_score = Column(Integer)  # 0-100
    
    # Per spec: Key Analysis Areas
    abusive_clauses = Column(JSONB)        # Cláusulas Abusivas
    payment_terms = Column(JSONB)          # Condições de Pagamento
    termination_conditions = Column(JSONB) # Prazos e Rescisão
    warranties_penalties = Column(JSONB)   # Garantias e Penalidades
    
    # Agent metadata (per llm_router.py + contract_analysis_service.py)
    agent_type = Column(String)  # classifier, rental, telecom, financial
    llm_model_used = Column(String)  # gemini-1.5-pro, claude-3-5-sonnet, etc
    llm_provider_used = Column(String)  # gemini_pro, anthropic_sonnet, etc
    complexity_level = Column(String)  # simples, medio, complexo, especializado
    rag_context_used = Column(JSONB)  # RAG citations for transparency
    processing_time_ms = Column(Integer)
    analysis_cost_usd = Column(Float)  # Track AI costs per contract
    
    # E-signature integration (D4Sign)
    signature_request_id = Column(String)
    signature_status = Column(String)
    signed_at = Column(DateTime)
    signed_by = Column(String)  # Email do assinante
    
    # Audit trail (LGPD compliance)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    analyzed_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="contracts")
    chat_messages = relationship("ChatMessage", back_populates="contract", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Contract {self.id} - {self.title} ({self.status.value})>"
