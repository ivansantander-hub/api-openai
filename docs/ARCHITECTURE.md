# Backend Architecture Documentation

## Overview

This OpenAI API Service has been refactored into a clean, modular architecture that separates concerns and enables easy scaling and maintenance.

## Project Structure

```
/
├── backend/                    # Main backend module
│   ├── __init__.py            # Backend package initialization
│   ├── main.py                # FastAPI application factory
│   ├── config/                # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py        # Environment settings & validation
│   ├── models/                # Pydantic models
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication models
│   │   ├── openai_models.py  # OpenAI request/response models
│   │   └── responses.py      # Common response models
│   ├── services/              # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py   # Authentication service
│   │   └── openai_service.py # OpenAI API integration
│   ├── routes/               # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── health.py        # Health check routes
│   │   └── openai.py        # OpenAI API routes
│   ├── middleware/          # Custom middleware
│   │   ├── __init__.py
│   │   └── auth_middleware.py # Authentication middleware
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── helpers.py       # Helper functions
├── public/                  # Frontend static files
│   ├── index.html
│   ├── style.css
│   └── script.js
├── main.py                  # Entry point for local development
├── Procfile                 # Railway deployment configuration
└── requirements.txt         # Python dependencies
```

## Components

### Configuration (`backend/config/`)

**settings.py** - Centralized configuration management
- Environment variable loading
- Configuration validation
- Settings class with typed properties
- Status checking methods

### Models (`backend/models/`)

**auth.py** - Authentication models
- `AuthRequest`: Login request validation
- `AuthResponse`: Authentication response structure

**openai_models.py** - OpenAI API models
- `ChatRequest`: Chat completion parameters
- `CompletionRequest`: Text completion parameters
- `ImageRequest`: Image generation parameters
- `EmbeddingRequest`: Embedding creation parameters

**responses.py** - Common response models
- `HealthResponse`: Health check response
- `ErrorResponse`: Standardized error format
- `SuccessResponse`: Generic success response
- `ModelsResponse`: Models list response

### Services (`backend/services/`)

**auth_service.py** - Authentication business logic
- User authentication with access key
- Token validation
- Security utilities

**openai_service.py** - OpenAI API integration
- Client initialization and management
- Chat completions
- Text completions
- Image generation
- Embeddings creation
- Models listing

### Routes (`backend/routes/`)

**auth.py** - Authentication endpoints
- `POST /auth` - User authentication

**health.py** - Health monitoring
- `GET /health` - Service health status

**openai.py** - OpenAI API endpoints (protected)
- `POST /chat` - Chat completions
- `POST /completion` - Text completions
- `POST /images/generate` - Image generation
- `POST /embeddings` - Create embeddings
- `GET /models` - List available models

### Middleware (`backend/middleware/`)

**auth_middleware.py** - Authentication middleware
- `verify_access_key()` - Required authentication
- `optional_auth()` - Optional authentication
- HTTPBearer token validation

### Utils (`backend/utils/`)

**helpers.py** - Utility functions
- Request ID generation
- Timestamp utilities
- Error response formatting
- String sanitization
- Model name validation

## API Endpoints

### Public Endpoints
- `GET /` - Frontend application
- `GET /health` - Health check
- `POST /auth` - Authentication

### Protected Endpoints (require Bearer token)
- `POST /chat` - Chat completion
- `POST /completion` - Text completion
- `POST /images/generate` - Image generation
- `POST /embeddings` - Create embeddings
- `GET /models` - List models

## Authentication Flow

1. **Frontend Login**: User enters access key
2. **Token Validation**: Backend validates against `ACCESS_KEY` environment variable
3. **Token Storage**: Frontend stores token in localStorage
4. **Request Authentication**: All protected endpoints require `Authorization: Bearer <token>` header
5. **Auto-logout**: Invalid tokens trigger automatic logout

## Environment Variables

### Required
- `ACCESS_KEY` - Authentication key for API access
- `OPENAI_API_KEY` - OpenAI API key

### Optional
- `PORT` - Server port (default: 8000)
- `LOG_LEVEL` - Logging level (default: INFO)

## Deployment

### Local Development
```bash
python main.py
```

### Railway Deployment
```bash
# Railway automatically uses the Procfile:
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

## Error Handling

- **Global Exception Handler**: Catches unhandled exceptions
- **Standardized Responses**: Consistent error format across all endpoints
- **Request Tracking**: Unique request IDs for debugging
- **Validation Errors**: Pydantic model validation with detailed messages

## Security Features

- **Access Key Authentication**: Simple but secure API access
- **Token-based Authorization**: Bearer token for session management
- **Input Sanitization**: String cleaning and validation
- **Model Validation**: Prevents invalid model names
- **CORS Configuration**: Configurable cross-origin policies

## Scalability Design

### Modular Architecture
- Clear separation of concerns
- Dependency injection ready
- Service-oriented design
- Easy to extend with new features

### Future Enhancements Ready
- JWT token implementation
- Database integration
- Caching layer
- Rate limiting
- Monitoring and metrics

### Non-OpenAI Services
The architecture is designed to easily accommodate additional AI services:

```python
# Example: Adding a new service
backend/
├── services/
│   ├── openai_service.py
│   ├── anthropic_service.py  # New service
│   └── huggingface_service.py
├── routes/
│   ├── openai.py
│   ├── anthropic.py          # New routes
│   └── huggingface.py
└── models/
    ├── openai_models.py
    ├── anthropic_models.py    # New models
    └── huggingface_models.py
```

## Development Guidelines

1. **Add new models** in appropriate files under `models/`
2. **Business logic** goes in `services/`
3. **API endpoints** in `routes/`
4. **Cross-cutting concerns** in `middleware/`
5. **Utility functions** in `utils/`
6. **Configuration** in `config/settings.py`

## Testing Strategy

- Unit tests for services
- Integration tests for routes
- Model validation tests
- Configuration tests
- Health check monitoring 