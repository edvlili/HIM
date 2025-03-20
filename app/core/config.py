from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Home Inventory Management API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for managing home inventories with product tracking capabilities"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/him_db"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]  # Frontend URL
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 