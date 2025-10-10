"""
Audit log model for LGPD compliance
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .database import Base


class AuditLog(Base):
    """
    Audit logs for LGPD compliance
    Per spec: Security Guidelines - document access tracking
    """
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Action details
    action = Column(String, nullable=False, index=True)  # view, download, analyze, sign, delete
    resource_type = Column(String, nullable=False)  # contract, user, payment
    resource_id = Column(UUID(as_uuid=True), index=True)
    
    # Request metadata (renamed from 'metadata' to avoid SQLAlchemy reserved word)
    request_metadata = Column(JSONB)  # Additional context
    ip_address = Column(String)
    user_agent = Column(Text)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog {self.id} - {self.action} on {self.resource_type}>"
