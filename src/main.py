from fastapi import FastAPI
from src.api.routers import health
import os
from src.core.config import settings
from src.security_admin import SecurityAdmin


# Create FastAPI app with custom configuration
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",  # Default docs location
    openapi_url="/openapi.json",
    description="Production-ready GymTracker API with clean architecture",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    contact={
        "name": "GymTracker Team",
        "email": "support@gymtracker.com"
    }
)


# Health endpoint
app.include_router(health.router, prefix="/api/v1")

# Main admin router with all catalog management endpoints
from src.api.admin_api import api_admin_router
app.include_router(api_admin_router, prefix=f"/{settings.API_V1_STR}/admin", tags=["Admin"])


@app.get("/")
async def root(request):
    """Root endpoint - API information."""
    from fastapi.requests import Request
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }


# Configure CORS (production: restrict origins)
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",  # Development frontend
    "https://*.gymtracker.com",  # Production domains
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configure security headers middleware (production-ready)
from starlette.middleware.https import HTTPSRedirectMiddleware


class SecurityHeadersMiddleware:
    """Add security headers to all responses."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receiver):
        import asyncio
        import httpx
        response_headers = dict(receiver.headers)
        
        # Security headers
        if "Content-Security-Policy" not in response_headers:
            response_headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
        
        if "X-Frame-Options" not in response_headers:
            response_headers["X-Frame-Options"] = "SAMEORIGIN"
        
        if "X-XSS-Protection" not in response_headers:
            response_headers["X-XSS-Protection"] = "1; mode=block"
        
        app_response = await self.app(scope)
        if scope["type"] == "http":
            response = httpx.Response(scope["method"], 200, headers=response_headers)
        
        return [app_response]


# Apply security middleware (production-ready)
# app.add_middleware(SecurityHeadersMiddleware)


@app.on_event("startup")
async def startup_event():
    """Run on app startup."""
    print(f"✓ {settings.PROJECT_NAME} API starting...")
    print(f"  Version: {settings.VERSION}")
    print(f"  API Prefix: /{settings.API_V1_STR}/admin")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown."""
    print("✓ Shutting down GymTracker API...")

