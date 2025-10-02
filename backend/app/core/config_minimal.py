"""
Configuração simplificada para desenvolvimento
Permite executar a aplicação com configurações mínimas
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator, Field


class Settings(BaseSettings):
    """Configurações da aplicação - Versão Mínima para Desenvolvimento"""
    
    # ========================================
    # DATABASE CONFIGURATION
    # ========================================
    DATABASE_URL: str
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_JWT_SECRET: Optional[str] = None
    DATABASE_PASSWORD: Optional[str] = None
    
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
    # AI SERVICES (Opcionais para início)
    # ========================================
    ANTHROPIC_API_KEY: Optional[str] = None
    CLAUDE_MODEL: str = "claude-3-sonnet-20240229"
    MAX_TOKENS: int = 4000
    
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = None
    GOOGLE_APPLICATION_CREDENTIALS_JSON: Optional[str] = None
    
    # ========================================
    # EXTERNAL SERVICES (Opcionais)
    # ========================================
    # Cloudflare R2
    CLOUDFLARE_R2_ACCESS_KEY_ID: Optional[str] = None
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: Optional[str] = None
    CLOUDFLARE_R2_BUCKET_NAME: str = "democratiza-ai-files"
    CLOUDFLARE_R2_PUBLIC_URL: Optional[str] = None
    
    # AWS SQS
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "sa-east-1"
    AWS_SQS_QUEUE_URL: Optional[str] = None
    
    # SendGrid
    SENDGRID_API_KEY: Optional[str] = None
    SENDGRID_FROM_EMAIL: str = "noreply@democratiza-ai.com.br"
    SENDGRID_FROM_NAME: str = "Democratiza AI"
    
    # ========================================
    # PAYMENT PROCESSING (Opcionais)
    # ========================================
    MERCADO_PAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADO_PAGO_PUBLIC_KEY: Optional[str] = None
    MERCADO_PAGO_WEBHOOK_SECRET: Optional[str] = None
    
    # D4Sign
    D4SIGN_API_TOKEN: Optional[str] = None
    D4SIGN_CRYPT_KEY: Optional[str] = None
    D4SIGN_BASE_URL: str = "https://secure.d4sign.com.br/api/v1"
    
    # ========================================
    # APPLICATION SETTINGS
    # ========================================
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Democratiza AI"
    
    # CORS
    BACKEND_CORS_ORIGINS: str = "http://localhost:3000,https://localhost:3000,http://127.0.0.1:3000,https://127.0.0.1:3000"
    
    # ========================================
    # COMPUTED PROPERTIES
    # ========================================
    @property
    def database_url_sync(self) -> str:
        """URL síncrona do banco para SQLAlchemy"""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://")
    
    @property
    def supabase_configured(self) -> bool:
        """Verifica se Supabase está configurado"""
        return bool(self.SUPABASE_URL and self.SUPABASE_ANON_KEY and self.SUPABASE_SERVICE_KEY)
    
    @property
    def ai_enabled(self) -> bool:
        """Verifica se IA está habilitada"""
        return bool(self.ANTHROPIC_API_KEY and not self.ANTHROPIC_API_KEY.startswith("[SUBSTITUA"))
    
    @property
    def ocr_enabled(self) -> bool:
        """Verifica se OCR está habilitado"""
        return bool(self.GOOGLE_CLOUD_PROJECT_ID and self.GOOGLE_APPLICATION_CREDENTIALS_JSON)
    
    @property
    def file_storage_enabled(self) -> bool:
        """Verifica se armazenamento de arquivos está habilitado"""
        return bool(self.CLOUDFLARE_R2_ACCESS_KEY_ID and self.CLOUDFLARE_R2_SECRET_ACCESS_KEY)
    
    @property
    def email_enabled(self) -> bool:
        """Verifica se envio de email está habilitado"""
        return bool(self.SENDGRID_API_KEY and not self.SENDGRID_API_KEY.startswith("[SUBSTITUA"))
    
    @property
    def payments_enabled(self) -> bool:
        """Verifica se pagamentos estão habilitados"""
        return bool(self.MERCADO_PAGO_ACCESS_TOKEN and not self.MERCADO_PAGO_ACCESS_TOKEN.startswith("[SUBSTITUA"))
    
    # ========================================
    # PYDANTIC CONFIG
    # ========================================
    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignorar variáveis extras


# Instância global das configurações
settings = Settings()


def get_settings() -> Settings:
    """Factory function para dependency injection"""
    return settings