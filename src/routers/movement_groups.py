from fastapi import APIRouter, Depends, status
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.movement_group_service import MovementGroupService
from src.schemas.catalog import MovementGroupCreate, MovementGroupUpdate, MovementGroupResponse
from src.core.errors import not_found

router = APIRouter(prefix="/movement-groups", tags=["Movement Groups"])


async def get_movement_group_service(db: AsyncSession = Depends(get_db)):
    return MovementGroupService(db)


@router.post("/", response_model=MovementGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_movement_group(
    in_data: MovementGroupCreate,
    service: MovementGroupService = Depends(get_movement_group_service)
):
    return await service.create(in_data=in_data.model_dump())


@router.get("/", response_model=List[MovementGroupResponse])
async def list_movement_groups(skip: int = 0, limit: int = 100, service: MovementGroupService = Depends(get_movement_group_service)):
    return await service.list(skip=skip, limit=limit)


@router.get("/{id}", response_model=MovementGroupResponse)
async def get_movement_group(
    id: UUID,
    service: MovementGroupService = Depends(get_movement_group_service)
):
    result = await service.get_by_id(id)
    if not result:
        raise not_found("Movement group not found")
    return result


@router.patch("/{id}", response_model=MovementGroupResponse)
async def update_movement_group(
    id: UUID,
    in_data: MovementGroupUpdate,
    service: MovementGroupService = Depends(get_movement_group_service)
):
    result = await service.update(id=id, in_data=in_data.model_dump(exclude_unset=True))
    if not result:
        raise not_found("Movement group not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movement_group(
    id: UUID,
    service: MovementGroupService = Depends(get_movement_group_service)
):
    if not await service.delete(id=id):
        raise not_found("Movement group not found")
    return None
