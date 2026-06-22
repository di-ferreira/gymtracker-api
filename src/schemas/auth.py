from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: str = Field(..., max_length=255, example="user@example.com")
    password: str = Field(..., min_length=8, max_length=128, example="securepass123")
    name: str = Field(..., max_length=150, example="John Doe")


class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: str = Field(..., max_length=255, example="user@example.com")
    password: str = Field(..., example="securepass123")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
