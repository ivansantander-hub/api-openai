"""
Utility functions and helpers.
"""

import uuid
from typing import Any, Dict, Optional
from datetime import datetime


def generate_request_id() -> str:
    """Generate a unique request ID."""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def format_error_response(error: Exception, request_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Format error response with consistent structure.
    
    Args:
        error: Exception that occurred
        request_id: Optional request ID for tracking
        
    Returns:
        Dict: Formatted error response
    """
    return {
        "error": type(error).__name__,
        "message": str(error),
        "timestamp": get_timestamp(),
        "request_id": request_id or generate_request_id()
    }


def format_success_response(
    data: Any, 
    message: str = "Operation completed successfully",
    request_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Format success response with consistent structure.
    
    Args:
        data: Response data
        message: Success message
        request_id: Optional request ID for tracking
        
    Returns:
        Dict: Formatted success response
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": get_timestamp(),
        "request_id": request_id or generate_request_id()
    }


def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string input by removing dangerous characters and limiting length.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        return str(text)
    
    # Remove null bytes and control characters
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized.strip()


def validate_model_name(model: str) -> bool:
    """
    Validate if model name follows expected patterns.
    
    Args:
        model: Model name to validate
        
    Returns:
        bool: True if valid model name
    """
    valid_prefixes = [
        "gpt-3.5",
        "gpt-4",
        "text-",
        "dall-e",
        "whisper",
        "tts"
    ]
    
    return any(model.startswith(prefix) for prefix in valid_prefixes) 