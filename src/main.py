from fastapi import FastAPI
from src.api.routers import health
import os
from src.core.config import settings


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


# Health endpoint - Registered first
app.include_router(health.router, prefix="/api/v1/admin")

# Main admin router with all catalog management endpoints  
from src.routers.admin_api import api_admin_router
app.include_router(api_admin_router, tags=["Admin"])


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "environment": "production" if not os.getenv("DEBUG") else "development"
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


@app.on_event("startup")
async def startup_event():
    """Run on app startup."""
    from fastapi import FastAPI
    app.logger.info(f"{settings.PROJECT_NAME} API starting version {settings.VERSION}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown."""
    app.logger.info("Shutting down GymTracker API...")
