from pydantic import BaseSettings

class Settings(BaseSettings):
    # Application settings
    app_name: str = "Democratiza AI"
    app_version: str = "1.0.0"
    
    # Database settings
    database_url: str
    database_echo: bool = False

    # API settings
    api_prefix: str = "/api/v1"
    
    # Security settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()