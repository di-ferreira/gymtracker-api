from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.core.dependencies import get_current_user
from src.schemas.auth import UserResponse
from src.schemas.workout import (
    WorkoutCreate, WorkoutUpdate, WorkoutResponse,
    WorkoutExerciseCreate, WorkoutExerciseUpdate, WorkoutExerciseResponse,
    WorkoutReorder,
)
from src.services.workout_service import WorkoutService
from src.core.errors import not_found, forbidden

router = APIRouter(prefix="/workouts", tags=["Workouts"])


async def get_service(db: AsyncSession = Depends(get_db)):
    return WorkoutService(db)


@router.get("/", response_model=List[WorkoutResponse])
async def list_workouts(
    skip: int = 0,
    limit: int = 100,
    user_id: UUID | None = None,
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    is_admin = current_user.role == "admin"

    if user_id is not None:
        if not is_admin:
            raise forbidden("Only admins can list workouts for other users")
        target_user_id = user_id
    elif is_admin:
        target_user_id = None
    else:
        target_user_id = current_user.id

    workouts, _ = await service.list_by_user(
        target_user_id, skip=skip, limit=min(limit, 100)
    )
    return workouts


@router.post("/", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(
    in_data: WorkoutCreate,
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    target_user_id = in_data.user_id or current_user.id
    if target_user_id != current_user.id and current_user.role != "admin":
        raise forbidden("Only admins can create workouts for other users")
    return await service.create(target_user_id, in_data)


@router.get("/{id}", response_model=WorkoutResponse)
async def get_workout(
    id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    result = await service.get_by_id(id, current_user.id, is_admin=current_user.role == "admin")
    if not result:
        raise not_found("Workout not found")
    return result


@router.patch("/{id}", response_model=WorkoutResponse)
async def update_workout(
    in_data: WorkoutUpdate,
    id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    result = await service.update(id, current_user.id, in_data, is_admin=current_user.role == "admin")
    if not result:
        raise not_found("Workout not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    if not await service.delete(id, current_user.id, is_admin=current_user.role == "admin"):
        raise not_found("Workout not found")
    return None


@router.post(
    "/{id}/exercises/",
    response_model=WorkoutExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_exercise_to_workout(
    in_data: WorkoutExerciseCreate,
    id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    result = await service.add_exercise(id, current_user.id, in_data, is_admin=current_user.role == "admin")
    if not result:
        raise not_found("Workout not found")
    return result


@router.patch(
    "/{id}/exercises/{exercise_id}",
    response_model=WorkoutExerciseResponse,
)
async def update_workout_exercise(
    in_data: WorkoutExerciseUpdate,
    id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    exercise_id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    result = await service.update_exercise(
        exercise_id, id, current_user.id, in_data, is_admin=current_user.role == "admin"
    )
    if not result:
        raise not_found("Workout exercise not found")
    return result


@router.delete(
    "/{id}/exercises/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_exercise_from_workout(
    id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    exercise_id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    if not await service.remove_exercise(exercise_id, id, current_user.id, is_admin=current_user.role == "admin"):
        raise not_found("Workout exercise not found")
    return None


@router.put("/{id}/exercises/reorder")
async def reorder_workout_exercises(
    in_data: WorkoutReorder,
    id: UUID = Path(..., examples=["550e8400-e29b-41d4-a716-446655440000"]),
    current_user: UserResponse = Depends(get_current_user),
    service: WorkoutService = Depends(get_service),
):
    if not await service.reorder_exercises(
        id, current_user.id, in_data.exercise_ids, is_admin=current_user.role == "admin"
    ):
        raise not_found("Workout not found")
    return {"status": "ok"}
