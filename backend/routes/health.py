"""
Health check routes.
"""

from fastapi import APIRouter
from ..models.responses import HealthResponse
from ..config.settings import settings
from ..services.openai_service import openai_service

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        HealthResponse: Current service health status
    """
    config_status = settings.validate_configuration()
    
    openai_status = "available" if openai_service.is_available else "unavailable"
    auth_status = "configured" if settings.is_auth_configured else "not configured"
    
    return HealthResponse(
        status="healthy",
        message=f"Service is operational. OpenAI: {openai_status}, Auth: {auth_status}",
        openai_client=openai_status,
        authentication=auth_status,
        service_version=settings.APP_VERSION
    ) 