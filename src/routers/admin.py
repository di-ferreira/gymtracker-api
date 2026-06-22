"""
Admin Router with authentication middleware and comprehensive error handling.
Provides secure access to catalog management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from starlette.responses import JSONResponse
from typing import Any, Dict, Optional
from datetime import datetime
import json

from src.core.config import settings
from src.security_admin import generate_token, validate_uuid


router = APIRouter(
    prefix="/admin/catalog",
    tags=["Catalog Management"],
)


# ==================== Security Headers Middleware ==================== #

async def apply_security_headers(response: Response):
    """Add security headers to all admin responses."""
    security_headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Content-Security-Policy": "default-src 'self'",
    }
    for header, value in security_headers.items():
        response.headers[header] = value
    
    # Rate limiting header (placeholder)
    if response.status_code == 429:
        response.headers["Retry-After"] = str(60)


# ==================== Authentication Check (Stub for Development) ==================== #

async def get_admin_user_stub() -> Dict[str, Any]:
    """
    Stub authentication function for development.
    
    TODO: Replace with JWT/OAuth2 token validation in production.
    """
    return {
        "role": "admin",
        "permissions": ["read", "write", "delete"],
        "username": "admin@example.com"
    }


# ==================== Error Handlers ==================== #

@router.exception_handler(HTTPException)
async def admin_http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent JSON responses."""
    
    detail = {
        "detail": str(exc.detail),
        "status_code": exc.status_code,
        "path": request.url.path,
        "method": request.method
    }
    
    if exc.status_code in [404]:
        response = Response(
            content=json.dumps(detail),
            status_code=exc.status_code,
            media_type="application/json"
        )
        await apply_security_headers(response)
    else:
        response = JSONResponse(
            status_code=exc.status_code,
            content=detail
        )
    
    return response


@router.exception_handler(Exception)
async def admin_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions with server error responses."""
    import traceback
    
    detail = {
        "detail": "Internal server error occurred",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "path": request.url.path
    }
    
    # Log the full exception (production: use proper logging)
    # print(traceback.format_exc())
    
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=detail
    )
    await apply_security_headers(response)
    
    return response


@router.exception_handler(ValidationError)
async def admin_validation_error_handler(request: Request, exc: ValidationError):
    """Handle validation errors gracefully."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": str(exc.detail),
            "status_code": 422
        }
    )


@router.exception_handler(AuthenticationError)
async def admin_auth_error_handler(request: Request, exc: AuthenticationError):
    """Handle authentication errors."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Authentication required",
            "status_code": 401
        }
    )
