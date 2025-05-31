"""
OpenAI-related Pydantic models.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChatMessage(BaseModel):
    """Individual chat message model."""
    role: str = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Request model for chat completion."""
    model: str = Field(default="gpt-3.5-turbo", description="Model to use for chat completion")
    messages: List[ChatMessage] = Field(..., description="List of messages in the conversation")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=1000, gt=0, description="Maximum number of tokens to generate")


class CompletionRequest(BaseModel):
    """Request model for text completion."""
    model: str = Field(default="gpt-3.5-turbo-instruct", description="Model to use for completion")
    prompt: str = Field(..., description="The prompt to complete")
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: Optional[int] = Field(default=100, gt=0, description="Maximum number of tokens to generate")


class ImageRequest(BaseModel):
    """Request model for image generation."""
    prompt: str = Field(..., description="Text description of the desired image")
    size: Optional[str] = Field(default="1024x1024", description="Size of the generated image")
    quality: Optional[str] = Field(default="standard", description="Quality of the generated image")
    n: Optional[int] = Field(default=1, ge=1, le=4, description="Number of images to generate")


class EmbeddingRequest(BaseModel):
    """Request model for text embeddings."""
    model: str = Field(default="text-embedding-ada-002", description="Model to use for embeddings")
    input: str = Field(..., description="Text to create embeddings for") 