"""
Common response models.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional, List


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service health status")
    message: str = Field(..., description="Health status message")
    openai_client: str = Field(..., description="OpenAI client status")
    authentication: str = Field(..., description="Authentication status")
    service_version: str = Field(..., description="Service version")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Any] = Field(None, description="Additional error details")


class SuccessResponse(BaseModel):
    """Generic success response model."""
    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    data: Optional[Any] = Field(None, description="Response data")


class ModelsResponse(BaseModel):
    """Models list response model."""
    models: List[Any] = Field(..., description="List of available models")
    count: int = Field(..., description="Number of models") 