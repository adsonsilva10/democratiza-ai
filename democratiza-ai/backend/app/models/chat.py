"""
Chat message model for WebSocket interface
"""

from sqlalchemy import Column, Text, DateTime, ForeignKey, Boolean, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from .database import Base


class ChatMessage(Base):
    """
    Chat messages for WebSocket interface
    Per spec: api/v1/chat.py with ChatWithAgent.tsx
    """
    __tablename__ = "chat_messages"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    contract_id = Column(UUID(as_uuid=True), ForeignKey("contracts.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Message content
    message = Column(Text, nullable=False)
    response = Column(Text)
    is_user = Column(Boolean, default=True)
    
    # RAG context for this specific Q&A
    rag_context = Column(JSONB)  # Citations from knowledge base
    
    # Agent metadata (which specialist answered + LLM used)
    agent_type = Column(String)  # rental, telecom, financial
    llm_model_used = Column(String)  # Which model answered
    response_time_ms = Column(Integer)
    response_cost_usd = Column(Float)  # Track costs per message
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    contract = relationship("Contract", back_populates="chat_messages")
    user = relationship("User", back_populates="chat_messages")
    
    def __repr__(self):
        return f"<ChatMessage {self.id} - {'User' if self.is_user else 'Agent'}>"
