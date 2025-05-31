"""
Main entry point for the OpenAI API Service.
"""

import uvicorn
from backend.main import app
from backend.config.settings import settings

if __name__ == "__main__":
    print(f"🚀 Starting {settings.APP_NAME}")
    print(f"📖 API Documentation: http://localhost:{settings.PORT}/docs")
    print(f"🔄 Redoc Documentation: http://localhost:{settings.PORT}/redoc")
    
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    ) 