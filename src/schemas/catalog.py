import re
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9\s-]", "", name.lower()).replace(" ", "-").strip("-")


class MuscleGroupBase(BaseModel):
    name: str = Field(..., max_length=150, example="Peitoral")

    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class MuscleGroupCreate(MuscleGroupBase):
    description: Optional[str] = Field(None, max_length=1000)
    order_index: Optional[int] = 0

    model_config = ConfigDict(validate_assignment=True)


class MuscleGroupUpdate(BaseModel):
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
    id: UUID
    description: Optional[str]
    order_index: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovementGroupBase(BaseModel):
    name: str = Field(..., max_length=150, example="Compound")

    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class MovementGroupCreate(MovementGroupBase):
    description: Optional[str] = Field(None, max_length=1000)
    order_index: Optional[int] = 0

    model_config = ConfigDict(validate_assignment=True)


class MovementGroupUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    slug: Optional[str] = Field(None)
    description: Optional[str] = None
    order_index: Optional[int] = None


class MovementGroupResponse(MovementGroupBase):
    id: UUID
    description: Optional[str]
    order_index: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EquipmentBase(BaseModel):
    name: str = Field(..., max_length=100, example="Dumbbell")

    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class EquipmentCreate(EquipmentBase):
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=50)
    order_index: Optional[int] = 0

    model_config = ConfigDict(validate_assignment=True)


class EquipmentUpdate(BaseModel):
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
    id: UUID
    description: Optional[str]
    category: Optional[str]
    order_index: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
