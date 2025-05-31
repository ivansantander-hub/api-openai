"""
Authentication middleware for API endpoints.
"""

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from ..services.auth_service import AuthService
from ..config.settings import settings


# Security scheme
security = HTTPBearer(auto_error=False)


def verify_access_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Verify access key from Authorization header.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        str: Validated token
        
    Raises:
        HTTPException: If authentication fails
    """
    if not settings.is_auth_configured:
        raise HTTPException(
            status_code=503,
            detail="Authentication not configured. Please set ACCESS_KEY."
        )
    
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Please provide access key."
        )
    
    if not AuthService.validate_token(credentials.credentials):
        raise HTTPException(
            status_code=403,
            detail="Invalid access key."
        )
    
    return credentials.credentials


def optional_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[str]:
    """
    Optional authentication for endpoints that can work without auth.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        Optional[str]: Token if valid, None otherwise
    """
    if not credentials or not settings.is_auth_configured:
        return None
    
    if AuthService.validate_token(credentials.credentials):
        return credentials.credentials
    
    return None 