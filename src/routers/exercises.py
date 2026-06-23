from fastapi import APIRouter, Depends, status, Query
from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.services.exercise_service import ExerciseService
from src.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse
from src.core.errors import not_found

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
    name: Optional[str] = Query(None, max_length=255),
    difficulty: Optional[str] = Query(None),
    search: Optional[str] = Query(None, max_length=255),
    muscle_group_ids: Optional[List[UUID]] = Query(None),
    movement_group_ids: Optional[List[UUID]] = Query(None),
    equipment_ids: Optional[List[UUID]] = Query(None),
    include: Optional[str] = Query(None, description="Comma-separated: instructions,alternatives"),
    order_by: str = Query("name"),
    order_dir: str = Query("asc"),
    service: ExerciseService = Depends(get_exercise_service)
):
    filters = {k: v for k, v in {
        "name": name,
        "difficulty": difficulty,
        "search": search,
        "muscle_group_ids": muscle_group_ids,
        "movement_group_ids": movement_group_ids,
        "equipment_ids": equipment_ids,
    }.items() if v is not None}
    include_list = include.split(",") if include else None
    exercises, _ = await service.list_exercises(
        skip=skip, limit=min(limit, 100),
        filters=filters if filters else None,
        order_by=order_by, order_dir=order_dir,
        include=include_list,
    )
    return exercises


@router.get("/{id}", response_model=ExerciseResponse)
async def get_exercise(
    id: UUID,
    include: Optional[str] = Query(None, description="Comma-separated: instructions,alternatives"),
    service: ExerciseService = Depends(get_exercise_service)
):
    include_list = include.split(",") if include else None
    result = await service.get_by_id(id, include=include_list)
    if not result:
        raise not_found("Exercise not found")
    return result


@router.patch("/{id}", response_model=ExerciseResponse)
async def update_exercise(
    id: UUID,
    in_data: ExerciseUpdate,
    service: ExerciseService = Depends(get_exercise_service)
):
    result = await service.update(id=id, in_data=in_data)
    if not result:
        raise not_found("Exercise not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    id: UUID,
    service: ExerciseService = Depends(get_exercise_service)
):
    if not await service.delete(id=id):
        raise not_found("Exercise not found")
    return None
