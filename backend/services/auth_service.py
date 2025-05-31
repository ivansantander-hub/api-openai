"""
Authentication service for user access control.
"""

from fastapi import HTTPException
from ..config.settings import settings
from ..models.auth import AuthRequest, AuthResponse


class AuthService:
    """Service for handling authentication operations."""
    
    @staticmethod
    def authenticate_user(auth_request: AuthRequest) -> AuthResponse:
        """
        Authenticate user with provided access key.
        
        Args:
            auth_request: Authentication request with access key
            
        Returns:
            AuthResponse: Authentication result
            
        Raises:
            HTTPException: If authentication fails or is not configured
        """
        if not settings.is_auth_configured:
            raise HTTPException(
                status_code=503,
                detail="Authentication not configured. Please set ACCESS_KEY."
            )
        
        if auth_request.access_key == settings.ACCESS_KEY:
            return AuthResponse(
                authenticated=True,
                message="Authentication successful",
                token=auth_request.access_key  # In production, use JWT tokens
            )
        else:
            raise HTTPException(
                status_code=403,
                detail="Invalid access key"
            )
    
    @staticmethod
    def validate_token(token: str) -> bool:
        """
        Validate authentication token.
        
        Args:
            token: Token to validate
            
        Returns:
            bool: True if token is valid
        """
        if not settings.is_auth_configured:
            return False
        
        return token == settings.ACCESS_KEY 