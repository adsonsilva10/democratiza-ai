"""
Schemas package - Pydantic models for API validation
"""

from .user import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    Token,
    PasswordReset,
    PasswordResetConfirm
)

from .contract import (
    ContractCreate,
    ContractUpload,
    ContractResponse,
    ContractDetail,
    ContractAnalysisRequest,
    ContractAnalysisResponse,
    ContractList,
    ContractAnalysisResult,
    AbusiveClause,
    PaymentTerms,
    TerminationConditions,
    WarrantiesPenalties,
    ContractTypeEnum,
    RiskLevelEnum,
    ContractStatusEnum
)

from .chat import (
    ChatMessageCreate,
    ChatMessageResponse,
    ChatHistoryResponse,
    ChatStreamChunk
)

__all__ = [
    # User schemas
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "Token",
    "PasswordReset",
    "PasswordResetConfirm",
    
    # Contract schemas
    "ContractCreate",
    "ContractUpload",
    "ContractResponse",
    "ContractDetail",
    "ContractAnalysisRequest",
    "ContractAnalysisResponse",
    "ContractList",
    "ContractAnalysisResult",
    "AbusiveClause",
    "PaymentTerms",
    "TerminationConditions",
    "WarrantiesPenalties",
    "ContractTypeEnum",
    "RiskLevelEnum",
    "ContractStatusEnum",
    
    # Chat schemas
    "ChatMessageCreate",
    "ChatMessageResponse",
    "ChatHistoryResponse",
    "ChatStreamChunk",
]
