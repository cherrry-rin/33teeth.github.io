from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "33 Зуб - Dental Clinic API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Server
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: list = ["*"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()