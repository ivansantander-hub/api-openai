"""
Main FastAPI application with modular architecture.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from .config.settings import settings
from .routes import auth, health, openai
from .utils.helpers import format_error_response


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(openai.router)
    
    # Mount static files
    try:
        app.mount(
            settings.STATIC_MOUNT_PATH, 
            StaticFiles(directory=settings.STATIC_DIR), 
            name="static"
        )
    except Exception as e:
        print(f"⚠️  Warning: Could not mount static files: {e}")
    
    # Root endpoint to serve frontend
    @app.get("/")
    async def serve_frontend():
        """Serve the main frontend page."""
        try:
            return FileResponse(f"{settings.STATIC_DIR}/index.html")
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, 
                detail="Frontend not found. Please ensure index.html exists in the public directory."
            )
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Handle uncaught exceptions globally."""
        error_response = format_error_response(exc)
        return HTTPException(
            status_code=500,
            detail=error_response
        )
    
    return app


# Create app instance
app = create_app()


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    # Validate configuration
    config_status = settings.validate_configuration()
    
    if config_status["warnings"]:
        print("⚠️  Configuration warnings:")
        for warning in config_status["warnings"]:
            print(f"   - {warning}")
    else:
        print("✅ All configurations are valid")
    
    print(f"🌐 Server will run on {settings.HOST}:{settings.PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    print("🛑 Shutting down OpenAI API Service")


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    ) 