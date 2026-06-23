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
    role: str = "user"
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: str = Field(..., max_length=255, example="user@example.com")
    password: str = Field(..., example="securepass123")


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=150, example="Novo Nome")
    current_password: Optional[str] = Field(None, min_length=8, max_length=128, example="oldpass123")
    new_password: Optional[str] = Field(None, min_length=8, max_length=128, example="newpass456")


class AdminUpdateUserRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    role: Optional[str] = Field(None, pattern="^(admin|user)$")
    is_active: Optional[bool] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
