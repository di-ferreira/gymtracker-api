"""Schemas for exercise instructions and alternatives."""

from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class InstructionBase(BaseModel):
    """Base fields for exercise instruction step."""
    description: str = Field(..., min_length=1, max_length=500)  # Reasonable limit
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "step_order" not in data:
            data["step_order"] = len([k for k in data.keys() if k.startswith("instruction_")]) + 1
        return data


class InstructionCreate(InstructionBase):
    """Schema for creating instruction step."""
    model_config = ConfigDict(extra='forbid')


class InstructionUpdate(BaseModel):
    """Schema for updating instruction step."""
    description: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class InstructionResponse(InstructionBase):
    """Response schema for instruction."""
    id: UUID
    exercise_id: UUID
    step_order: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class AlternativeBase(BaseModel):
    """Base fields for exercise alternative."""
    # Note: The primary_key='alternative_exercise_id' is handled at DB level
    note: Optional[str] = Field(None, max_length=1000)
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "exercise_id" not in data and "note" in data:
            # Default exercise_id based on context (would need to be passed explicitly)
            pass
        return data


class AlternativeCreate(BaseModel):
    """Schema for creating exercise alternative."""
    model_config = ConfigDict(extra='forbid')  # All fields must be positional


class AlternativeResponse(BaseModel):
    """Response schema for alternative."""
    id: UUID
    exercise_id: UUID
    alternative_exercise_id: UUID
    reason: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
