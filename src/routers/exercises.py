"""Exercise Router with full CRUD operations."""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.services.exercise_service import ExerciseService
from src.models.exercise import ExerciseResponse

router = APIRouter(prefix="/exercises", tags=["Exercises"])


async def get_exercise_service(db: AsyncSession = Depends(get_db)):
    return ExerciseService(db)


@router.post(
    "/", 
    response_model=ExerciseResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Create an exercise",
    tags=["Exercises"]
)
async def create_exercise(
    in_data: dict,
    service: ExerciseService = Depends(get_exercise_service)
):
    """
    Create a new exercise.
    
    - All fields optional except movement_group_id and muscle_group_id
    - Slug auto-generated from name if not provided
    """
    return await service.create(in_data=in_data)


@router.get(
    "/", 
    summary="List exercises",
    tags=["Exercises"]
)
async def list_exercises(
    skip: int = 0,
    limit: int = 100,
    service: ExerciseService = Depends(get_exercise_service)
):
    """List exercises with pagination (limited to first page)."""
    exercises, _ = await service.list_exercises(skip=skip, limit=min(limit, 100))
    
    # Only return exercises matching the skip/limit
    offset = min(skip + 1, len(exercises)) if exercises.skip else min(1, len(exercises)) if exercises.skip else 0
    
    response_items = []
    for ex in exercises[:offset]:
        response_items.append(ExerciseResponse.model_validate(ex))
    
    return response_items


@router.get("/{id}", response_model=ExerciseResponse)
async def get_exercise(
    id: UUID,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Get exercise by ID."""
    result = await service.get_by_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return result


@router.patch("/{id}", response_model=ExerciseResponse)
async def update_exercise(
    id: UUID,
    in_data: dict,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Update exercise by ID."""
    result = await service.update(id=id, in_data=in_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    id: UUID,
    service: ExerciseService = Depends(get_exercise_service)
):
    """Soft delete an exercise (mark as deleted)."""
    if not await service.delete(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return None
