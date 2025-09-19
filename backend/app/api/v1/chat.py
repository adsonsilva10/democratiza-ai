from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import uuid

from app.db.database import get_db
from app.db.models import ChatSession, ChatMessage, User, Contract
from app.api.v1.auth import get_current_user
from app.agents.factory import AgentFactory
from app.core.config import settings

router = APIRouter()

# Pydantic models
class ChatSessionCreate(BaseModel):
    title: Optional[str] = "Nova Conversa"
    contract_id: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    contract_id: Optional[str]
    is_active: bool
    created_at: datetime
    message_count: int

class ChatMessageCreate(BaseModel):
    content: str
    session_id: str

class ChatMessageResponse(BaseModel):
    id: str
    content: str
    role: str
    message_type: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]]

class ChatResponse(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_personal_message(self, message: str, session_id: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_text(message)

manager = ConnectionManager()

# Chat endpoints
@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create new chat session"""
    
    # Verify contract ownership if contract_id provided
    if session_data.contract_id:
        result = await db.execute(
            select(Contract)
            .where(Contract.id == session_data.contract_id, Contract.owner_id == current_user.id)
        )
        contract = result.scalar_one_or_none()
        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )
    
    # Create chat session
    chat_session = ChatSession(
        user_id=current_user.id,
        contract_id=session_data.contract_id,
        title=session_data.title
    )
    
    db.add(chat_session)
    await db.commit()
    await db.refresh(chat_session)
    
    return ChatSessionResponse(
        id=str(chat_session.id),
        title=chat_session.title,
        contract_id=str(chat_session.contract_id) if chat_session.contract_id else None,
        is_active=chat_session.is_active,
        created_at=chat_session.created_at,
        message_count=0
    )

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_chat_sessions(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's chat sessions"""
    
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(ChatSession.updated_at.desc())
    )
    sessions = result.scalars().all()
    
    # Get message counts for each session
    session_responses = []
    for session in sessions:
        message_result = await db.execute(
            select(ChatMessage).where(ChatMessage.session_id == session.id)
        )
        message_count = len(message_result.scalars().all())
        
        session_responses.append(ChatSessionResponse(
            id=str(session.id),
            title=session.title,
            contract_id=str(session.contract_id) if session.contract_id else None,
            is_active=session.is_active,
            created_at=session.created_at,
            message_count=message_count
        ))
    
    return session_responses

@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_chat_messages(
    session_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get messages from a chat session"""
    
    # Verify session ownership
    session_result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == session_id, ChatSession.user_id == current_user.id)
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    # Get messages
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .offset(skip)
        .limit(limit)
        .order_by(ChatMessage.created_at.asc())
    )
    messages = result.scalars().all()
    
    return [
        ChatMessageResponse(
            id=str(message.id),
            content=message.content,
            role=message.role,
            message_type=message.message_type,
            created_at=message.created_at,
            metadata=message.metadata
        )
        for message in messages
    ]

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_chat_message(
    session_id: str,
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send message to chat session and get AI response"""
    
    # Verify session ownership
    session_result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == session_id, ChatSession.user_id == current_user.id)
    )
    session = session_result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    # Save user message
    user_message = ChatMessage(
        session_id=session.id,
        content=message_data.content,
        role="user",
        message_type="text"
    )
    
    db.add(user_message)
    await db.commit()
    await db.refresh(user_message)
    
    try:
        # Generate AI response
        ai_response = await generate_ai_response(session, message_data.content, db)
        
        # Save AI message
        ai_message = ChatMessage(
            session_id=session.id,
            content=ai_response["message"],
            role="assistant",
            message_type="text",
            metadata=ai_response.get("context")
        )
        
        db.add(ai_message)
        await db.commit()
        await db.refresh(ai_message)
        
        # Send response via WebSocket if connected
        await manager.send_personal_message(
            json.dumps({
                "type": "ai_response",
                "message": ai_response["message"],
                "message_id": str(ai_message.id)
            }),
            session_id
        )
        
        return ChatMessageResponse(
            id=str(ai_message.id),
            content=ai_message.content,
            role=ai_message.role,
            message_type=ai_message.message_type,
            created_at=ai_message.created_at,
            metadata=ai_message.metadata
        )
        
    except Exception as e:
        # Return error message
        error_message = ChatMessage(
            session_id=session.id,
            content="Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.",
            role="assistant",
            message_type="error",
            metadata={"error": str(e)}
        )
        
        db.add(error_message)
        await db.commit()
        await db.refresh(error_message)
        
        return ChatMessageResponse(
            id=str(error_message.id),
            content=error_message.content,
            role=error_message.role,
            message_type=error_message.message_type,
            created_at=error_message.created_at,
            metadata=error_message.metadata
        )

async def generate_ai_response(session: ChatSession, message: str, db: AsyncSession) -> Dict[str, Any]:
    """Generate AI response using appropriate agent"""
    
    context = {"session_id": str(session.id)}
    
    # If session has a contract, get contract context
    if session.contract_id:
        contract_result = await db.execute(
            select(Contract).where(Contract.id == session.contract_id)
        )
        contract = contract_result.scalar_one_or_none()
        
        if contract and contract.extracted_text:
            # Use agent factory to get appropriate agent
            agent_factory = AgentFactory(None, None)  # TODO: Initialize with proper clients
            
            try:
                # For now, return a simple response
                # TODO: Implement proper agent integration
                response = f"Entendi sua pergunta sobre o contrato '{contract.title}'. "
                response += "Esta funcionalidade está sendo implementada e em breve você poderá "
                response += "conversar diretamente sobre os detalhes do seu contrato."
                
                context["contract_id"] = str(contract.id)
                context["contract_type"] = contract.contract_type
                
            except Exception as e:
                response = "Desculpe, ocorreu um erro ao analisar seu contrato. Tente novamente."
                context["error"] = str(e)
        else:
            response = "Este contrato ainda não foi analisado. Aguarde o processamento ser concluído."
    else:
        # General legal advice
        response = "Olá! Sou seu assistente especializado em contratos brasileiros. "
        response += "Como posso ajudá-lo hoje? Você pode fazer upload de um contrato para análise "
        response += "ou tirar dúvidas gerais sobre direitos do consumidor."
    
    return {
        "message": response,
        "context": context
    }

# WebSocket endpoint
@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time chat"""
    
    await manager.connect(websocket, session_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Echo message back (for development)
            await manager.send_personal_message(
                json.dumps({
                    "type": "echo",
                    "message": message_data.get("message", "")
                }),
                session_id
            )
            
    except WebSocketDisconnect:
        manager.disconnect(session_id)

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete chat session"""
    
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == session_id, ChatSession.user_id == current_user.id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    await db.delete(session)
    await db.commit()
    
    return {"message": "Chat session deleted successfully"}
