"""
OpenAI service for AI model interactions.
"""

from typing import Any, Dict, List
from fastapi import HTTPException
import openai

from ..config.settings import settings
from ..models.openai_models import (
    ChatRequest, 
    CompletionRequest, 
    ImageRequest, 
    EmbeddingRequest
)


class OpenAIService:
    """Service for handling OpenAI API operations."""
    
    def __init__(self):
        """Initialize OpenAI service with client setup."""
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize OpenAI client if API key is available."""
        if settings.is_openai_configured:
            try:
                self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                print("✅ OpenAI client initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing OpenAI client: {e}")
                self.client = None
        else:
            print("⚠️  WARNING: OpenAI API key not configured")
    
    def _check_client(self) -> None:
        """Check if OpenAI client is available."""
        if self.client is None:
            raise HTTPException(
                status_code=503,
                detail="OpenAI client not available. Please configure OPENAI_API_KEY."
            )
    
    def chat_completion(self, request: ChatRequest) -> Dict[str, Any]:
        """
        Generate chat completion using OpenAI.
        
        Args:
            request: Chat completion request
            
        Returns:
            Dict containing the chat response
            
        Raises:
            HTTPException: If OpenAI API fails
        """
        self._check_client()
        
        try:
            response = self.client.chat.completions.create(
                model=request.model,
                messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return {
                "message": response.choices[0].message.content,
                "model": request.model,
                "usage": response.usage.model_dump() if response.usage else None,
                "id": response.id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    
    def text_completion(self, request: CompletionRequest) -> Dict[str, Any]:
        """
        Generate text completion using OpenAI.
        
        Args:
            request: Text completion request
            
        Returns:
            Dict containing the completion response
            
        Raises:
            HTTPException: If OpenAI API fails
        """
        self._check_client()
        
        try:
            response = self.client.completions.create(
                model=request.model,
                prompt=request.prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            
            return {
                "text": response.choices[0].text,
                "model": request.model,
                "usage": response.usage.model_dump() if response.usage else None,
                "id": response.id
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    
    def generate_image(self, request: ImageRequest) -> Dict[str, Any]:
        """
        Generate image using DALL-E.
        
        Args:
            request: Image generation request
            
        Returns:
            Dict containing the image response
            
        Raises:
            HTTPException: If OpenAI API fails
        """
        self._check_client()
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=request.prompt,
                size=request.size,
                quality=request.quality,
                n=request.n
            )
            
            return {
                "url": response.data[0].url,
                "prompt": request.prompt,
                "size": request.size,
                "quality": request.quality,
                "revised_prompt": getattr(response.data[0], 'revised_prompt', None)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    
    def create_embeddings(self, request: EmbeddingRequest) -> Dict[str, Any]:
        """
        Create embeddings using OpenAI.
        
        Args:
            request: Embedding creation request
            
        Returns:
            Dict containing the embeddings response
            
        Raises:
            HTTPException: If OpenAI API fails
        """
        self._check_client()
        
        try:
            response = self.client.embeddings.create(
                model=request.model,
                input=request.input
            )
            
            return {
                "embeddings": [data.embedding for data in response.data],
                "model": request.model,
                "usage": response.usage.model_dump() if response.usage else None
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    
    def list_models(self) -> Dict[str, Any]:
        """
        List available OpenAI models.
        
        Returns:
            Dict containing the models list
            
        Raises:
            HTTPException: If OpenAI API fails
        """
        self._check_client()
        
        try:
            response = self.client.models.list()
            models = [model.model_dump() for model in response.data]
            
            return {
                "models": models,
                "count": len(models)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    
    @property
    def is_available(self) -> bool:
        """Check if OpenAI service is available."""
        return self.client is not None


# Global service instance
openai_service = OpenAIService() 