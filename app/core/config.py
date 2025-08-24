"""
Core configuration settings for the FastAPI application.
"""
from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    """Application settings."""
    
    app_name: str = "FastAPI Demo Server"
    app_version: str = "1.0.0"
    app_description: str = "A comprehensive FastAPI backend server demo"
    debug: bool = True
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    
    # Security
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database (for demo purposes, using in-memory storage)
    database_url: Optional[str] = None
    
    # CORS
    allowed_origins: list = ["http://localhost:3000", "http://localhost:8080"]


settings = Settings()
