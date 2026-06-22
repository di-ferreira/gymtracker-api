from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class MuscleGroupBase(BaseModel):
    name: str = Field(..., max_length=100, example="Peitoral")
    slug: str = Field(..., max_length=100, example="peitoral")

class MuscleGroupCreate(MuscleGroupBase):
    pass

class MuscleGroupUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=100)

class MuscleGroupResponse(MuscleGroupBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
