from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from src.schemas.exercise import ExerciseResponse


class WorkoutExerciseBase(BaseModel):
    sort_order: int = Field(default=0, ge=0)
    sets: Optional[int] = Field(None, ge=1)
    reps: Optional[int] = Field(None, ge=1)
    weight: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class WorkoutExerciseCreate(WorkoutExerciseBase):
    exercise_id: UUID


class WorkoutExerciseUpdate(BaseModel):
    sort_order: Optional[int] = Field(None, ge=0)
    sets: Optional[int] = Field(None, ge=1)
    reps: Optional[int] = Field(None, ge=1)
    weight: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = None


class WorkoutExerciseResponse(WorkoutExerciseBase):
    id: UUID
    workout_id: UUID
    exercise_id: UUID
    exercise: Optional[ExerciseResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WorkoutReorder(BaseModel):
    exercise_ids: List[UUID] = Field(..., description="Ordered list of workout exercise IDs")


class WorkoutCreate(BaseModel):
    name: str = Field(..., max_length=255)
    notes: Optional[str] = None
    user_id: Optional[UUID] = Field(
        None, description="ID do usuário alvo (apenas admin pode definir)"
    )


class WorkoutUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class WorkoutResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    notes: Optional[str] = None
    exercises: List[WorkoutExerciseResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
