"""Muscle Group Router for gym catalog management."""

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.muscle_group_service import MuscleGroupService
from src.models.exercise import MuscleGroupResponse

router = APIRouter(prefix="/muscle-groups", tags=["Muscle Groups"])


async def get_muscle_group_service(db: AsyncSession = Depends(get_db)):
    return MuscleGroupService(db)


@router.post("/", response_model=MuscleGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_muscle_group(
    in_data: dict, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    """Create a new muscle group."""
    return await service.create(in_data=in_data)


@router.get("/")
async def list_muscle_groups(skip: int = 0, limit: int = 100, service: MuscleGroupService = Depends(get_muscle_group_service)):
    """List muscle groups with pagination."""
    groups, _ = await service.list(skip=skip, limit=min(limit, 100))
    return groups


@router.get("/{id}", response_model=MuscleGroupResponse)
async def get_muscle_group(
    id: UUID, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    """Get muscle group by ID."""
    result = await service.get_by_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Muscle group not found")
    return result


@router.patch("/{id}", response_model=MuscleGroupResponse)
async def update_muscle_group(
    id: UUID, 
    in_data: dict, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    """Update muscle group by ID."""
    result = await service.update(id=id, in_data=in_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Muscle group not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_muscle_group(
    id: UUID, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    """Soft delete muscle group."""
    if not await service.delete(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Muscle group not found")
    return None
