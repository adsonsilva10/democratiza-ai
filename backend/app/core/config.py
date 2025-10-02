import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
from functools import lru_cache

class Settings(BaseSettings):
    """
    Configurações da aplicação Democratiza AI
    Carrega variáveis de ambiente com validação
    """
    
    # ========================================
    # DATABASE CONFIGURATION
    # ========================================
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # ========================================
    # JWT CONFIGURATION
    # ========================================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY deve ter pelo menos 32 caracteres")
        return v
    
    # ========================================
    # AI SERVICES
    # ========================================
    ANTHROPIC_API_KEY: str
    CLAUDE_MODEL: str = "claude-3-sonnet-20240229"
    MAX_TOKENS: int = 4000
    
    GOOGLE_CLOUD_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    
    # ========================================
    # EXTERNAL SERVICES
    # ========================================
    # Cloudflare R2
    CLOUDFLARE_R2_ACCOUNT_ID: str
    CLOUDFLARE_R2_ACCESS_KEY_ID: str
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: str
    CLOUDFLARE_R2_BUCKET_NAME: str
    CLOUDFLARE_R2_PUBLIC_URL: str
    
    # AWS SQS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "sa-east-1"
    AWS_SQS_QUEUE_URL: str
    
    # SendGrid
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SENDGRID_FROM_NAME: str = "Democratiza AI"
    
    # ========================================
    # PAYMENT PROCESSING
    # ========================================
    MERCADO_PAGO_ACCESS_TOKEN: str
    MERCADO_PAGO_PUBLIC_KEY: str
    MERCADO_PAGO_WEBHOOK_SECRET: str
    
    # D4Sign
    D4SIGN_API_KEY: Optional[str] = None
    D4SIGN_CRYPTO_KEY: Optional[str] = None
    D4SIGN_BASE_URL: str = "https://secure.d4sign.com.br/api/v1"
    
    # ========================================
    # APPLICATION SETTINGS
    # ========================================
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Democratiza AI"
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    BACKEND_CORS_ORIGINS: List[str] = []
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_MINUTES: int = 1
    
    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_TYPES: str = "pdf,jpg,jpeg,png,gif,txt"
    
    @property
    def allowed_file_types_list(self) -> List[str]:
        return [ext.strip() for ext in self.ALLOWED_FILE_TYPES.split(",")]
    
    @property
    def max_file_size_bytes(self) -> int:
        return self.MAX_FILE_SIZE_MB * 1024 * 1024
    
    # ========================================
    # LOGGING & MONITORING
    # ========================================
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str] = None
    
    # ========================================
    # COMPUTED PROPERTIES
    # ========================================
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def database_url_sync(self) -> str:
        """Versão síncrona da URL do banco para SQLAlchemy"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    
    @property
    def database_url_async(self) -> str:
        """Versão assíncrona da URL do banco para AsyncSQLAlchemy"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True
    
    # File Upload
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FILE_TYPES: List[str] = ["application/pdf", "image/jpeg", "image/png", "image/webp"]
    
    # AI Configuration
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    # Application Base URL (for webhooks)
    API_BASE_URL: str = "https://yourdomain.com"  # Update in production
    
    # RAG Configuration
    EMBEDDING_DIMENSION: int = 1536
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
