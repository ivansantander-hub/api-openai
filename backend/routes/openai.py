"""
OpenAI API routes.
"""

from fastapi import APIRouter, Depends
from typing import Any, Dict

from ..models.openai_models import (
    ChatRequest, 
    CompletionRequest, 
    ImageRequest, 
    EmbeddingRequest
)
from ..models.responses import ModelsResponse
from ..services.openai_service import openai_service
from ..middleware.auth_middleware import verify_access_key

router = APIRouter(tags=["OpenAI"])


@router.post("/chat")
async def chat_completion(
    request: ChatRequest, 
    token: str = Depends(verify_access_key)
) -> Dict[str, Any]:
    """
    Generate chat completion using OpenAI.
    
    Args:
        request: Chat completion request
        token: Authentication token
        
    Returns:
        Dict containing the chat response
    """
    return openai_service.chat_completion(request)


@router.post("/completion")
async def text_completion(
    request: CompletionRequest, 
    token: str = Depends(verify_access_key)
) -> Dict[str, Any]:
    """
    Generate text completion using OpenAI.
    
    Args:
        request: Text completion request
        token: Authentication token
        
    Returns:
        Dict containing the completion response
    """
    return openai_service.text_completion(request)


@router.post("/images/generate")
async def generate_image(
    request: ImageRequest, 
    token: str = Depends(verify_access_key)
) -> Dict[str, Any]:
    """
    Generate image using DALL-E.
    
    Args:
        request: Image generation request
        token: Authentication token
        
    Returns:
        Dict containing the image response
    """
    return openai_service.generate_image(request)


@router.post("/embeddings")
async def create_embeddings(
    request: EmbeddingRequest, 
    token: str = Depends(verify_access_key)
) -> Dict[str, Any]:
    """
    Create embeddings using OpenAI.
    
    Args:
        request: Embedding creation request
        token: Authentication token
        
    Returns:
        Dict containing the embeddings response
    """
    return openai_service.create_embeddings(request)


@router.get("/models")
async def list_models(
    token: str = Depends(verify_access_key)
) -> Dict[str, Any]:
    """
    List available OpenAI models.
    
    Args:
        token: Authentication token
        
    Returns:
        Dict containing the models list
    """
    return openai_service.list_models() 