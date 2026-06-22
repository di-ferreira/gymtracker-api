"""
Pydantic schemas for GymTracker API validation and response serialization.
Includes pagination, filtering, and nested response schemas."""

import re
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator, StringConstraints


def slugify(name: str) -> str:
    """Helper to generate safe slugs from names."""
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r"[^a-z0-9\s-]", "", name.lower())
    slug = re.sub(r"\s+", "-", slug).strip("-")
    return slug


class BaseResponse(BaseModel):
    """Base response schema with common fields."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class PaginationInfo(BaseModel):
    """Pagination metadata for list responses."""
    page: int = Field(..., ge=1, description="Current page number (1-indexed)")
    per_page: int = Field(..., ge=1, le=100, description="Items per page (max 100)")
    total_pages: int = Field(description="Total number of pages")
    has_previous: bool = Field(description="Whether previous page exists")
    has_next: bool = Field(description="Whether next page exists")
    total_items: int = Field(description="Total items matching the query")


class ExerciseFilter(BaseModel):
    """
    Filter criteria for exercise listing.
    
    Supports filtering by muscle group, movement group, difficulty, equipment, etc.
    """
    name: Optional[str] = Field(None, max_length=255)
    slug: Optional[str] = Field(None)
    difficulty: Optional[Optional[str]] = Field(None)  # Nullable Enum for flexibility
    muscle_group_ids: Optional[List[UUID]] = Field(None)
    movement_group_ids: Optional[List[UUID]] = Field(None)
    equipment_ids: Optional[List[UUID]] = Field(None)
    search: Optional[str] = Field(None, max_length=255)  # Fuzzy text search


class ExerciseSearch(BaseModel):
    """
    Search criteria for exercise searching.
    
    Supports full-text search across multiple fields.
    """
    query: str = Field(..., min_length=1, max_length=255, description="Search query")
    enable_fuzzy_match: Optional[bool] = True


class ExerciseSort(BaseModel):
    """Sorting options for exercise listing."""
    field: str = Field("name", description='Field to sort by (e.g., "name", "difficulty")')
    order: str = Field("asc", description='Sort order ("asc" or "desc")')


class ExercisePaginate(BaseModel):
    """Pagination parameters for exercise listing."""
    skip: Optional[int] = 0  # Number of items to skip
    limit: Optional[int] = 100  # Items per page (max 100)
    search: Optional[str] = None
    search_type: Optional[str] = Field("simple", description='Search type: "simple" or "fuzzy"')


class ExerciseBase(BaseModel):
    """Base fields for exercise."""
    name: StringConstraints(max_length=255) = Field(..., example="Supino Mentado")
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        # Auto-generate slug if not provided
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class ExerciseCreate(BaseExerciseBase):
    """Schema for creating a new exercise."""
    description: Optional[str] = Field(None)
    execution_tips: Optional[str] = Field(None)
    difficulty: Optional[Optional[str]] = Field(None)  # Nullable Enum
    thumbnail_url: Optional[str] = Field(None)
    image_url: Optional[str] = Field(None)
    gif_url: Optional[str] = Field(None)
    video_url: Optional[str] = Field(None)
    movement_group_id: UUID = Field(..., description="Required: Movement group ID")
    muscle_group_id: UUID = Field(..., description="Required: Muscle group ID")
    
    model_config = ConfigDict(validate_assignment=True)


class ExerciseUpdate(BaseExerciseBase):
    """Schema for updating an existing exercise."""
    # All fields optional except id (handled in router)
    description: Optional[str] = None
    execution_tips: Optional[str] = None
    difficulty: Optional[Optional[str]] = None
    thumbnail_url: Optional[str] = None
    image_url: Optional[str] = None
    gif_url: Optional[str] = None
    video_url: Optional[str] = None
    
    @classmethod
    def model_fields_set(cls, data: dict) -> dict:
        if "slug" not in data and "name" in data:
            data["slug"] = slugify(data["name"])
        return data


class ExerciseResponse(BaseExerciseBase):
    """Response schema for exercises."""
    id: UUID
    movement_group_id: UUID
    muscle_group_id: UUID
    
    # Model config to automatically populate from DB model
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
