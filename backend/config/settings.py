"""
Application settings and configuration.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings class."""
    
    # API Information
    APP_NAME: str = "OpenAI API Service"
    APP_DESCRIPTION: str = "A comprehensive FastAPI service for OpenAI integrations"
    APP_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", 8000))
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Authentication Configuration
    ACCESS_KEY: Optional[str] = os.getenv("ACCESS_KEY")
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Static Files
    STATIC_DIR: str = "public"
    STATIC_MOUNT_PATH: str = "/static"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def is_openai_configured(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.OPENAI_API_KEY)
    
    @property
    def is_auth_configured(self) -> bool:
        """Check if authentication is configured."""
        return bool(self.ACCESS_KEY)
    
    def validate_configuration(self) -> dict:
        """Validate current configuration and return status."""
        status = {
            "openai_configured": self.is_openai_configured,
            "auth_configured": self.is_auth_configured,
            "warnings": []
        }
        
        if not self.is_openai_configured:
            status["warnings"].append("OpenAI API key not configured")
        
        if not self.is_auth_configured:
            status["warnings"].append("Access key not configured")
        
        return status


# Global settings instance
settings = Settings() 