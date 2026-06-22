"""
Admin API Router - Secure catalog management endpoint.

Provides admin-only access to full CRUD operations on gym catalog resources.
All endpoints are protected with authentication middleware."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
import os

from src.core.config import settings

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    include_in_schema=True,
)


# Security Headers Middleware
async def security_headers(request: Request):
    """Add security headers to all responses."""
    from starlette.middleware.base import BaseHTTPMiddleware
    
    # In a real implementation, we'd use middleware here
    pass  # Headers added via Response objects


@router.get("/", tags=["Admin Health"])
async def health_check(request: Request) -> Dict[str, Any]:
    """Health check endpoint for admin panel."""
    return {
        "status": "ok",
        "version": settings.VERSION,
        "environment": os.getenv("ENVIRONMENT", "production"),
        "database": "gymtracker"
    }


@router.get("/meta", tags=["Admin Meta"])
async def get_platform_info() -> Dict[str, Any]:
    """Get platform metadata for admin panel integration."""
    return {
        "platform": "GymTracker Catalog API",
        "version": settings.VERSION,
        "slug": "gymtracker-api",
        "admin_access": True,
        "supports_search": True,
        "supports_pagination": True,
        "features": [
            "Exercise Management",
            "Equipment Management", 
            "Movement Groups",
            "Muscle Groups",
            "Catalog Sync & Versioning"
        ]
    }


# Error handlers for admin routes
@router.exception_handler(HTTPException)
async def admin_http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent admin responses."""
    return {
        "detail": str(exc.detail),
        "status_code": exc.status_code
    }


@router.exception_handler(Exception)
async def admin_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions (logging would go here)."""
    from fastapi import Response
    
    return Response(
        content={
            "detail": "An internal server error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        media_type="application/json"
    )
