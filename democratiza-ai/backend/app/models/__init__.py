"""
Models package - Database entities
Per spec: PostgreSQL via Supabase with pg_vector extension
"""

from .database import Base, engine, SessionLocal, get_db
from .user import User
from .contract import Contract, ContractType, RiskLevel, ContractStatus
from .chat import ChatMessage
from .audit_log import AuditLog

__all__ = [
    # Database
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    
    # Models
    "User",
    "Contract",
    "ChatMessage",
    "AuditLog",
    
    # Enums
    "ContractType",
    "RiskLevel",
    "ContractStatus",
]
