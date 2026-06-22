"""Schemas for equipment and muscle group entities."""

import re
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator, StringConstraints


def slugify(name: str) -> str:
    """Helper to generate safe slugs from names."""
    return re.sub(r"[^a-z0-9\s-]", "", name.lower()).replace(" ", "-").strip("-")


class MuscleGroupBase(BaseModel):
    """Base fields for muscle group."""
    name: StringConstraints(max_length=150) = Field(..., example="Peitoral")
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class MuscleGroupCreate(MuscleGroupBase):
    """Schema for creating a muscle group."""
    description: Optional[str] = Field(None, max_length=1000)
    order_index: Optional[int] = 0
    
    model_config = ConfigDict(validate_assignment=True)


class MuscleGroupUpdate(BaseModel):
    """Schema for updating muscle group."""
    name: Optional[str] = Field(None, max_length=150)
    slug: Optional[str] = Field(None)
    description: Optional[str] = None
    order_index: Optional[int] = None
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class MuscleGroupResponse(MuscleGroupBase):
    """Response schema for muscle groups."""
    id: UUID
    description: Optional[str]
    order_index: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class MovementGroupBase(BaseModel):
    """Base fields for movement group."""
    name: StringConstraints(max_length=150) = Field(..., example="Compound")
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class MovementGroupCreate(MovementGroupBase):
    """Schema for creating a movement group."""
    description: Optional[str] = Field(None, max_length=1000)
    order_index: Optional[int] = 0
    
    model_config = ConfigDict(validate_assignment=True)


class MovementGroupUpdate(BaseModel):
    """Schema for updating movement group."""
    name: Optional[str] = Field(None, max_length=150)
    slug: Optional[str] = Field(None)
    description: Optional[str] = None
    order_index: Optional[int] = None


class MovementGroupResponse(MovementGroupBase):
    """Response schema for movement groups."""
    id: UUID
    description: Optional[str]
    order_index: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class EquipmentBase(BaseModel):
    """Base fields for equipment."""
    name: StringConstraints(max_length=100) = Field(..., example="Dumbbell")
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class EquipmentCreate(EquipmentBase):
    """Schema for creating equipment."""
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=50)
    order_index: Optional[int] = 0
    
    model_config = ConfigDict(validate_assignment=True)


class EquipmentUpdate(BaseModel):
    """Schema for updating equipment."""
    name: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None)
    description: Optional[str] = None
    category: Optional[str] = None
    order_index: Optional[int] = None
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class EquipmentResponse(EquipmentBase):
    """Response schema for equipment."""
    id: UUID
    description: Optional[str]
    category: Optional[str]
    order_index: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
