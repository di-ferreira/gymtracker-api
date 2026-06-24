from fastapi import APIRouter, Depends, Security
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.exercise_service import ExerciseService
from src.services.muscle_group_service import MuscleGroupService
from src.services.movement_group_service import MovementGroupService
from src.services.equipment_service import EquipmentService
from src.schemas.exercise import ExerciseResponse, PaginatedExerciseResponse
from src.schemas.catalog import (
    MuscleGroupResponse, MovementGroupResponse, EquipmentResponse,
)
from src.core.dependencies import require_auth, get_current_user
from src.schemas.auth import UserResponse

router = APIRouter(prefix="/catalog", tags=["Public Catalog"])


async def get_exercise_service(db: AsyncSession = Depends(get_db)):
    return ExerciseService(db)

async def get_muscle_group_service(db: AsyncSession = Depends(get_db)):
    return MuscleGroupService(db)

async def get_movement_group_service(db: AsyncSession = Depends(get_db)):
    return MovementGroupService(db)

async def get_equipment_service(db: AsyncSession = Depends(get_db)):
    return EquipmentService(db)


@router.get("/exercises/", response_model=PaginatedExerciseResponse)
async def list_exercises(
    skip: int = 0,
    limit: int = 100,
    service: ExerciseService = Depends(get_exercise_service),
    _: dict = Security(require_auth),
):
    exercises, pagination = await service.list_exercises(skip=skip, limit=min(limit, 100))
    return PaginatedExerciseResponse(data=exercises, pagination=pagination)


@router.get("/muscle-groups/", response_model=List[MuscleGroupResponse])
async def list_muscle_groups(
    skip: int = 0,
    limit: int = 100,
    service: MuscleGroupService = Depends(get_muscle_group_service),
    _: dict = Security(require_auth),
):
    return await service.list_muscle_groups(skip, limit)


@router.get("/movement-groups/", response_model=List[MovementGroupResponse])
async def list_movement_groups(
    skip: int = 0,
    limit: int = 100,
    service: MovementGroupService = Depends(get_movement_group_service),
    _: dict = Security(require_auth),
):
    return await service.list(skip=skip, limit=limit)


@router.get("/equipment/", response_model=List[EquipmentResponse])
async def list_equipment(
    skip: int = 0,
    limit: int = 100,
    service: EquipmentService = Depends(get_equipment_service),
    _: dict = Security(require_auth),
):
    return await service.list(skip=skip, limit=limit)
