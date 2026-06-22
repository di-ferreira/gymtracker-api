"""
Security utilities for GymTracker API.
Provides authentication middleware, validation, and security helpers.
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional, Callable
from functools import wraps
from uuid import UUID


class SecurityError(Exception):
    """Base security exception."""
    pass


class AuthenticationError(SecurityError):
    """Raised when authentication fails."""
    pass


class AuthorizationError(SecurityError):
    """Raised when authorization fails."""
    pass


class ValidationError(SecurityError):
    """Raised when validation fails."""
    pass


def generate_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)


def validate_uuid(value: str) -> UUID:
    """Validate and parse UUID."""
    try:
        return UUID(value, version=4)
    except ValueError:
        raise ValidationError("Invalid UUID format")


def generate_slug(name: str) -> str:
    """Generate a URL-safe slug from a name."""
    import re
    # Convert to lowercase and remove special characters
    slug = "".join(
        char.lower() if char.isalnum() else "-"
        for char in str(name).strip().title().replace(" ", "-")
    )
    # Replace multiple dashes with single dash and trim
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def get_admin_user():
    """
    Dependency to ensure admin user authentication.
    
    Note: In production, replace this with actual JWT or OAuth2 authentication.
    This is a stub for development/preview API access.
    """
    # TODO: Implement proper JWT/OAuth2 authentication
    return {
        "role": "admin",
        "permissions": ["*"]  # Admin has access to all endpoints
    }


async def admin_required(dependency_func):
    """
    Dependency wrapper to require admin role.
    
    Args:
        dependency_func: The dependency function that returns user info
        
    Returns:
        Request user with admin role validated
    """
    from fastapi import HTTPException, status
    
    # Placeholder for actual authentication check
    # In production, integrate with JWT or OAuth2
    return {"role": "admin", "permissions": ["*"]}


def check_permission(user_permissions: list[str], required_permission: str) -> bool:
    """
    Check if user has required permission.
    
    Args:
        user_permissions: List of user's permissions (e.g., ["read", "write"])
        required_permission: Permission to check (e.g., "read:equipment")
        
    Returns:
        True if user has permission, False otherwise
    """
    # Admin users bypass permission checks
    if "*" in user_permissions or "admin" in user_permissions:
        return True
    
    # Check explicit permission match
    required_base = required_permission.split(":")[0]  # Get permission type part
    return any(required_base in perm for perm in user_permissions)
