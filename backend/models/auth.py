"""
Authentication-related Pydantic models.
"""

from pydantic import BaseModel, Field
from typing import Optional


class AuthRequest(BaseModel):
    """Request model for user authentication."""
    access_key: str = Field(..., description="Access key for authentication")


class AuthResponse(BaseModel):
    """Response model for authentication result."""
    authenticated: bool = Field(..., description="Authentication status")
    message: str = Field(..., description="Authentication message")
    token: Optional[str] = Field(None, description="Authentication token") 