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
    DATABASE_URL: Optional[str] = None
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_KEY: Optional[str] = None
    
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
    # OpenAI API
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Anthropic Claude API
    ANTHROPIC_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-3-sonnet-20240229"
    
    # Google Gemini API
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_FLASH_MODEL: str = "gemini-1.5-flash"
    GEMINI_PRO_MODEL: str = "gemini-1.5-pro"
    
    # Google Cloud (for OCR)
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    
    # AI Configuration
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    # ========================================
    # EXTERNAL SERVICES
    # ========================================
    # Cloudflare R2
    CLOUDFLARE_ACCOUNT_ID: Optional[str] = None
    CLOUDFLARE_R2_ACCESS_KEY: Optional[str] = None
    CLOUDFLARE_R2_SECRET_KEY: Optional[str] = None
    CLOUDFLARE_R2_BUCKET: Optional[str] = None
    CLOUDFLARE_R2_ENDPOINT: Optional[str] = None
    
    # AWS SQS
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "sa-east-1"
    AWS_SQS_QUEUE_URL: Optional[str] = None
    
    # SendGrid
    SENDGRID_API_KEY: Optional[str] = None
    SENDGRID_FROM_EMAIL: Optional[str] = None
    SENDGRID_FROM_NAME: str = "Democratiza AI"
    
    # ========================================
    # PAYMENT PROCESSING
    # ========================================
    MERCADO_PAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADO_PAGO_PUBLIC_KEY: Optional[str] = None
    MERCADO_PAGO_WEBHOOK_SECRET: Optional[str] = None
    
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
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if v is None or v == "":
            return "http://localhost:3000,http://127.0.0.1:3000"
        return v
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Converte string CORS em lista"""
        return [url.strip() for url in self.BACKEND_CORS_ORIGINS.split(",") if url.strip()]
    
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
    def database_url_async(self) -> str:
        """Versão assíncrona da URL do banco para AsyncSQLAlchemy"""
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
        return None

    @property
    def database_url_sync(self) -> str:
        """Versão síncrona da URL do banco para SQLAlchemy"""
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
        return None
    
    # RAG Configuration
    EMBEDDING_DIMENSION: int = 1536
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Application Base URL (for webhooks)
    API_BASE_URL: str = "http://localhost:8000"
    
    class Config:
        env_file = [".env", ".env.dev", ".env.local", ".env.private"]
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = "ignore"  # Ignora campos extras em vez de dar erro

settings = Settings()
