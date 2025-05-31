"""
Main FastAPI application with modular architecture.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
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
        redoc_url="/redoc",
        # Configuraciones específicas para Railway
        redirect_slashes=False,  # Evita redirects automáticos
        root_path="",  # Path root explícito
    )
    
    # Middleware para Railway - Trusted Host
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["*"]  # Railway maneja esto automáticamente
    )
    
    # Configure CORS con configuraciones específicas para Railway
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
        # Headers adicionales para Railway
        expose_headers=["*"],
        max_age=3600,
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
    
    # Middleware para debugging en Railway
    @app.middleware("http")
    async def log_requests(request, call_next):
        print(f"🔄 Request: {request.method} {request.url}")
        print(f"📡 Headers: {dict(request.headers)}")
        response = await call_next(request)
        print(f"✅ Response: {response.status_code}")
        return response
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        """Handle uncaught exceptions globally."""
        print(f"❌ Unhandled exception: {exc}")
        error_response = format_error_response(exc)
        return HTTPException(
            status_code=500,
            detail=error_response
        )
    
    return app


# Crear la instancia de la aplicación
app = create_app()

# Startup event para Railway
@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.APP_NAME} starting...")
    print(f"🔧 Environment: {'Railway' if settings.PORT != 8000 else 'Local'}")
    print(f"🔐 Auth configured: {settings.is_auth_configured}")
    print(f"🤖 OpenAI configured: {settings.is_openai_configured}")


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,  # Disable reload en producción
        log_level="info"
    ) 