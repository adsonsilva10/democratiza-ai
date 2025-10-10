"""
Pydantic schemas for Contract model
Aligned with contract_analysis_service.py output structure
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class ContractTypeEnum(str, Enum):
    """Contract types"""
    RENTAL = "rental"
    TELECOM = "telecom"
    FINANCIAL = "financial"
    EMPLOYMENT = "employment"
    SERVICE = "service"
    OTHER = "other"


class RiskLevelEnum(str, Enum):
    """Risk levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class ContractStatusEnum(str, Enum):
    """Contract processing statuses"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    CLASSIFYING = "classifying"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    SIGNED = "signed"
    ARCHIVED = "archived"
    ERROR = "error"


# Analysis sub-schemas (aligned with contract_analysis_service.py)

class AbusiveClause(BaseModel):
    """Abusive clause detection"""
    clause: str = Field(..., description="Text of the abusive clause")
    article: str = Field(..., description="CDC article violated")
    severity: str = Field(..., description="Severity: high, medium, low")
    explanation: str = Field(..., description="Simple language explanation")


class PaymentTerms(BaseModel):
    """Payment terms analysis"""
    total_value: Optional[str] = None
    installments: Optional[str] = None
    interest_rate: Optional[str] = None
    late_fees: Optional[str] = None
    concerns: List[str] = Field(default_factory=list)


class TerminationConditions(BaseModel):
    """Termination conditions analysis"""
    notice_period: Optional[str] = None
    penalties: Optional[str] = None
    concerns: List[str] = Field(default_factory=list)


class WarrantiesPenalties(BaseModel):
    """Warranties and penalties"""
    warranties: List[str] = Field(default_factory=list)
    penalties: List[str] = Field(default_factory=list)
    concerns: List[str] = Field(default_factory=list)


class ContractAnalysisResult(BaseModel):
    """
    Complete contract analysis result
    Matches contract_analysis_service.py output
    """
    risk_level: RiskLevelEnum
    risk_score: int = Field(..., ge=0, le=100, description="Risk score 0-100")
    abusive_clauses: List[AbusiveClause] = Field(default_factory=list)
    payment_terms: Optional[PaymentTerms] = None
    termination_conditions: Optional[TerminationConditions] = None
    warranties_penalties: Optional[WarrantiesPenalties] = None
    recommendations: List[str] = Field(default_factory=list)
    summary: str = Field(..., description="Executive summary in clear Portuguese")


# Request/Response schemas

class ContractCreate(BaseModel):
    """Schema for creating a new contract"""
    title: str = Field(..., min_length=1, max_length=255)
    file_name: str
    file_size: int = Field(..., gt=0)


class ContractUpload(BaseModel):
    """Schema for contract upload response"""
    contract_id: str
    file_url: str
    status: ContractStatusEnum


class ContractResponse(BaseModel):
    """Basic contract response"""
    id: str
    user_id: str
    title: str
    contract_type: Optional[ContractTypeEnum]
    status: ContractStatusEnum
    risk_level: RiskLevelEnum
    risk_score: Optional[int] = None
    file_url: str
    file_name: Optional[str] = None
    created_at: datetime
    analyzed_at: Optional[datetime] = None
    
    # LLM Router metadata
    llm_model_used: Optional[str] = None
    llm_provider_used: Optional[str] = None
    complexity_level: Optional[str] = None
    analysis_cost_usd: Optional[float] = None
    
    class Config:
        from_attributes = True


class ContractDetail(ContractResponse):
    """Detailed contract response with analysis"""
    extracted_text: Optional[str] = None
    analysis_result: Optional[ContractAnalysisResult] = None
    abusive_clauses: Optional[List[AbusiveClause]] = None
    payment_terms: Optional[PaymentTerms] = None
    termination_conditions: Optional[TerminationConditions] = None
    ocr_confidence: Optional[float] = None
    ocr_method: Optional[str] = None
    processing_time_ms: Optional[int] = None


class ContractAnalysisRequest(BaseModel):
    """Request for contract analysis"""
    contract_id: str
    analysis_depth: str = Field(default="standard", description="quick, standard, detailed, comprehensive")
    force_model: Optional[str] = None
    include_rag: bool = Field(default=True, description="Include RAG context")


class ContractAnalysisResponse(BaseModel):
    """Response from contract analysis"""
    contract_id: str
    analysis_summary: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    legal_insights: Dict[str, Any]
    recommendations: List[str]
    cost_breakdown: Dict[str, Any]
    processing_metadata: Dict[str, Any]


class ContractList(BaseModel):
    """Paginated list of contracts"""
    contracts: List[ContractResponse]
    total: int
    page: int
    page_size: int
