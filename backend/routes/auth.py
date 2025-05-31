"""
Authentication routes.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from ..models.auth import AuthRequest, AuthResponse
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/", response_model=AuthResponse)
@router.post("", response_model=AuthResponse)  # Sin trailing slash para Railway
async def authenticate(request: AuthRequest, req: Request):
    """
    Authenticate user with access key.
    
    Args:
        request: Authentication request with access key
        req: FastAPI Request object for debugging
        
    Returns:
        AuthResponse: Authentication result with token
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Log para debugging en Railway
        print(f"🔐 Auth request from: {req.client.host if req.client else 'unknown'}")
        print(f"📡 Request method: {req.method}")
        print(f"🔗 Request URL: {req.url}")
        print(f"📋 Headers: {dict(req.headers)}")
        
        result = AuthService.authenticate_user(request)
        
        # Respuesta explícita JSON para evitar redirects
        return JSONResponse(
            status_code=200,
            content={
                "authenticated": result.authenticated,
                "message": result.message,
                "token": result.token
            },
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
        
    except Exception as e:
        print(f"❌ Auth error: {str(e)}")
        raise e 