"""
Configurações para ambiente de desenvolvimento
Sem dependências de APIs externas
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
import os

class DevSettings(BaseSettings):
    """Configurações simplificadas para desenvolvimento"""
    
    # Application Settings
    APP_NAME: str = "Contrato Seguro - Dev"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    # Security (valores padrão para desenvolvimento)
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database (SQLite para desenvolvimento)
    DATABASE_URL: str = "sqlite:///./contracts_dev.db"
    
    # Mock Mode Flags
    USE_MOCK_RAG: bool = True
    USE_MOCK_OCR: bool = True
    USE_MOCK_LLM: bool = True
    USE_MOCK_SIGNATURES: bool = True
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: List[str] = ["application/pdf", "image/jpeg", "image/png", "image/webp"]
    
    # AI Configuration (para modo mock)
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    # RAG Configuration
    EMBEDDING_DIMENSION: int = 1536
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Development Storage (local)
    UPLOAD_DIR: str = "./uploads"
    
    class Config:
        env_file = ".env.dev"
        case_sensitive = True

# Instância global
dev_settings = DevSettings()

# Compatibilidade com o sistema existente
settings = dev_settings