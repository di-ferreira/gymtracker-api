from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.muscle_group_service import MuscleGroupService
from src.schemas.catalog import MuscleGroupCreate, MuscleGroupUpdate, MuscleGroupResponse
from src.core.errors import not_found

router = APIRouter(prefix="/muscle-groups", tags=["Muscle Groups"])


async def get_muscle_group_service(db: AsyncSession = Depends(get_db)):
    return MuscleGroupService(db)


@router.post("/", response_model=MuscleGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_muscle_group(
    in_data: MuscleGroupCreate,
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    return await service.create_muscle_group(in_data)


@router.get("/", response_model=List[MuscleGroupResponse])
async def list_muscle_groups(skip: int = 0, limit: int = 100, service: MuscleGroupService = Depends(get_muscle_group_service)):
    return await service.list_muscle_groups(skip, limit)


@router.get("/{id}", response_model=MuscleGroupResponse)
async def get_muscle_group(
    id: UUID,
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    result = await service.get_muscle_group(id)
    if not result:
        raise not_found("Muscle group not found")
    return result


@router.patch("/{id}", response_model=MuscleGroupResponse)
async def update_muscle_group(
    id: UUID,
    in_data: MuscleGroupUpdate,
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    result = await service.update_muscle_group(id, in_data)
    if not result:
        raise not_found("Muscle group not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_muscle_group(
    id: UUID,
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    if not await service.delete_muscle_group(id):
        raise not_found("Muscle group not found")
    return None
