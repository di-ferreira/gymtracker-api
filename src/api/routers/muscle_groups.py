from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.muscle_group_service import MuscleGroupService
from src.schemas.muscle_group import MuscleGroupCreate, MuscleGroupUpdate, MuscleGroupResponse

router = APIRouter(prefix="/muscle-groups", tags=["Muscle Groups"])

async def get_muscle_group_service(db: AsyncSession = Depends(get_db)) -> MuscleGroupService:
    return MuscleGroupService(db)

@router.post("/", response_model=MuscleGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_muscle_group(
    data: MuscleGroupCreate, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    return await service.create_muscle_group(data)

@router.get("/{id}", response_model=MuscleGroupResponse)
async def get_muscle_group(
    id: UUID, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    result = await service.get_muscle_group(id)
    if not result:
        raise HTTPException(status_code=404, detail="Muscle group not found")
    return result

@router.get("/", response_model=List[MuscleGroupResponse])
async def list_muscle_groups(
    skip: int = 0, 
    limit: int = 100, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    return await service.list_muscle_groups(skip, limit)

@router.patch("/{id}", response_model=MuscleGroupResponse)
async def update_muscle_group(
    id: UUID, 
    data: MuscleGroupUpdate, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    result = await service.update_muscle_group(id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Muscle group not found")
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_muscle_group(
    id: UUID, 
    service: MuscleGroupService = Depends(get_muscle_group_service)
):
    if not await service.delete_muscle_group(id):
        raise HTTPException(status_code=404, detail="Muscle group not found")
    return None
