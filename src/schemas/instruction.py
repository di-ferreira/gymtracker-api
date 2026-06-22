from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class InstructionCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    step_order: int = 0
    image_url: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class InstructionUpdate(BaseModel):
    description: Optional[str] = None
    step_order: Optional[int] = None
    image_url: Optional[str] = None


class InstructionResponse(BaseModel):
    id: UUID
    exercise_id: UUID
    step_order: int
    description: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AlternativeCreate(BaseModel):
    alternative_exercise_id: UUID
    reason: Optional[str] = Field(None, max_length=500)
    note: Optional[str] = Field(None, max_length=1000)

    model_config = ConfigDict(extra="forbid")


class AlternativeResponse(BaseModel):
    id: UUID
    exercise_id: UUID
    alternative_exercise_id: UUID
    reason: Optional[str] = None
    note: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
