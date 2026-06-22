"""Admin Authentication Middleware module."""

from typing import Optional, Callable
from datetime import datetime, timedelta
import secrets
import bcrypt


class SecurityError(Exception):
    """Base security exception."""
    pass


class AuthenticationError(SecurityError):
    """Raised when authentication fails."""
    pass


class ValidationError(SecurityError):
    """Raised when validation fails."""
    pass


def generate_token(length: int = 32) -> str:
    """Generate a secure random token."""
    return secrets.token_urlsafe(length)


def validate_uuid(value: str) -> bool:
    """Validate UUID format (basic check)."""
    import uuid
    try:
        uuid.UUID(value, version=4)
        return True
    except ValueError:
        return False


def generate_slug(name: str) -> str:
    """Generate URL-safe slug from name (remove special chars, lowercase)."""
    import re
    slug = re.sub(r"[^a-z0-9\s-]", "", name.lower())
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug
