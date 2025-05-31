"""
Authentication routes.
"""

from fastapi import APIRouter, HTTPException
from ..models.auth import AuthRequest, AuthResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/", response_model=AuthResponse)
async def authenticate(request: AuthRequest):
    """
    Authenticate user with access key.
    
    Args:
        request: Authentication request with access key
        
    Returns:
        AuthResponse: Authentication result with token
        
    Raises:
        HTTPException: If authentication fails
    """
    return AuthService.authenticate_user(request) 