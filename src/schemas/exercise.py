import re
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from src.schemas.catalog import MuscleGroupResponse, MovementGroupResponse, EquipmentResponse
from src.schemas.instruction import InstructionResponse, AlternativeResponse



def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9\s-]", "", name.lower())
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug


class PaginationInfo(BaseModel):
    page: int = Field(..., ge=1, description="Current page number")
    per_page: int = Field(..., ge=1, le=100, description="Items per page")
    total_pages: int = Field(description="Total number of pages")
    has_previous: bool = Field(description="Whether previous page exists")
    has_next: bool = Field(description="Whether next page exists")
    total_items: int = Field(description="Total items matching query")


class PaginatedExerciseResponse(BaseModel):
    data: List["ExerciseResponse"]
    pagination: PaginationInfo


class ExerciseFilter(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None)
    difficulty: Optional[str] = Field(None)
    muscle_group_ids: Optional[List[UUID]] = Field(None)
    movement_group_ids: Optional[List[UUID]] = Field(None)
    equipment_ids: Optional[List[UUID]] = Field(None)
    search: Optional[str] = Field(None, max_length=255)


class ExerciseBase(BaseModel):
    name: str = Field(..., max_length=255, example="Supino Mentado")

    model_config = ConfigDict(from_attributes=True)


class ExerciseCreate(ExerciseBase):
    description: Optional[str] = Field(None)
    execution_tips: Optional[str] = Field(None)
    difficulty: Optional[str] = Field(None)
    thumbnail_url: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    gif_url: Optional[str] = Field(None)
    video_url: Optional[str] = Field(None)
    movement_group_id: UUID = Field(..., description="Required: Movement group ID")
    muscle_group_id: UUID = Field(..., description="Required: Muscle group ID")
    equipment_ids: List[UUID] = Field(default_factory=list, description="Equipment IDs to associate")

    model_config = ConfigDict(validate_assignment=True)


class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None)
    description: Optional[str] = None
    execution_tips: Optional[str] = None
    difficulty: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_url: Optional[str] = None
    gif_url: Optional[str] = None
    video_url: Optional[str] = None
    equipment_ids: Optional[List[UUID]] = Field(None, description="Replace equipment associations")

    model_config = ConfigDict(from_attributes=True)


class ExerciseResponse(ExerciseBase):
    id: UUID
    slug: str
    description: Optional[str] = None
    execution_tips: Optional[str] = None
    difficulty: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_url: Optional[str] = None
    gif_url: Optional[str] = None
    video_url: Optional[str] = None
    movement_group_id: UUID
    muscle_group_id: UUID
    muscle_group: Optional[MuscleGroupResponse] = None
    movement_group: Optional[MovementGroupResponse] = None
    equipment: List[EquipmentResponse] = []
    instructions: Optional[List[InstructionResponse]] = None
    alternatives: Optional[List[AlternativeResponse]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
