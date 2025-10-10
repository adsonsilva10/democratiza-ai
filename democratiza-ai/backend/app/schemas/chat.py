"""
Pydantic schemas for ChatMessage model
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class ChatMessageCreate(BaseModel):
    """Schema for creating a chat message"""
    contract_id: str
    message: str = Field(..., min_length=1, max_length=10000)


class ChatMessageResponse(BaseModel):
    """Schema for chat message response"""
    id: str
    contract_id: str
    user_id: str
    message: str
    response: Optional[str] = None
    is_user: bool
    agent_type: Optional[str] = None
    llm_model_used: Optional[str] = None
    response_time_ms: Optional[int] = None
    response_cost_usd: Optional[float] = None
    rag_context: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Schema for chat history"""
    contract_id: str
    messages: list[ChatMessageResponse]
    total_messages: int


class ChatStreamChunk(BaseModel):
    """Schema for streaming chat responses"""
    chunk: str
    is_complete: bool = False
    metadata: Optional[Dict[str, Any]] = None
