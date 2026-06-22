from fastapi import APIRouter, Depends, HTTPException, status, Request
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.services.exercise_service import ExerciseService
from src.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse

router = APIRouter(prefix="/exercises", tags=["Exercises"])


async def get_exercise_service(db: AsyncSession = Depends(get_db)):
    return ExerciseService(db)


@router.post(
    "/",
    response_model=ExerciseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an exercise",
)
async def create_exercise(
    in_data: ExerciseCreate,
    service: ExerciseService = Depends(get_exercise_service)
):
    return await service.create(in_data=in_data)


@router.get(
    "/",
    response_model=List[ExerciseResponse],
    summary="List exercises",
)
async def list_exercises(
    skip: int = 0,
    limit: int = 100,
    service: ExerciseService = Depends(get_exercise_service)
):
    exercises, _ = await service.list_exercises(skip=skip, limit=min(limit, 100))
    return exercises


@router.get("/{id}", response_model=ExerciseResponse)
async def get_exercise(
    id: UUID,
    service: ExerciseService = Depends(get_exercise_service)
):
    result = await service.get_by_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return result


@router.patch("/{id}", response_model=ExerciseResponse)
async def update_exercise(
    id: UUID,
    in_data: ExerciseUpdate,
    service: ExerciseService = Depends(get_exercise_service)
):
    result = await service.update(id=id, in_data=in_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    id: UUID,
    service: ExerciseService = Depends(get_exercise_service)
):
    if not await service.delete(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return None
