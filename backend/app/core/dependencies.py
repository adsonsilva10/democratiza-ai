"""
Dependency Injection para FastAPI
Fornece instâncias compartilhadas de serviços
"""

from typing import Generator, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.database import get_db
from app.services.ocr_service import OCRService
from app.services.storage_service import StorageService
from app.core.security import verify_token
from app.db.models import User

# Security
security = HTTPBearer()

# Singleton instances
_ocr_service: Optional[OCRService] = None
_storage_service: Optional[StorageService] = None


def get_ocr_service() -> OCRService:
    """
    Dependency para obter instância do OCR Service (singleton)
    """
    global _ocr_service
    if _ocr_service is None:
        _ocr_service = OCRService()
    return _ocr_service


def get_storage_service() -> StorageService:
    """
    Dependency para obter instância do Storage Service (singleton)
    """
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency para obter o usuário atual autenticado
    Valida o token JWT e retorna o usuário do banco
    """
    token = credentials.credentials
    
    # Verificar e decodificar token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    # Buscar usuário no banco
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency que garante que o usuário está ativo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    return current_user
