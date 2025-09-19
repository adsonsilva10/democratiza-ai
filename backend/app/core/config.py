from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator
import os

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Contrato Seguro"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str
    
    # External APIs
    CLAUDE_API_KEY: str
    GOOGLE_CLOUD_VISION_API_KEY: str
    D4SIGN_API_KEY: str
    MERCADO_PAGO_ACCESS_TOKEN: str
    SENDGRID_API_KEY: str
    
    # AWS Services
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    SQS_QUEUE_URL: str
    
    # Cloudflare R2
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_ENDPOINT_URL: str
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "https://localhost:3000"]
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: List[str] = ["application/pdf", "image/jpeg", "image/png", "image/webp"]
    
    # AI Configuration
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    # RAG Configuration
    EMBEDDING_DIMENSION: int = 1536
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
