"""Movement Group Router for gym catalog management."""

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.movement_group_service import MovementGroupService
from src.models.exercise import MovementGroupResponse

router = APIRouter(prefix="/movement-groups", tags=["Movement Groups"])


async def get_movement_group_service(db: AsyncSession = Depends(get_db)):
    return MovementGroupService(db)


@router.post("/", response_model=MovementGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_movement_group(
    in_data: dict, 
    service: MovementGroupService = Depends(get_movement_group_service)
):
    """Create a new movement group."""
    return await service.create(in_data=in_data)


@router.get("/")
async def list_movement_groups(skip: int = 0, limit: int = 100, service: MovementGroupService = Depends(get_movement_group_service)):
    """List movement groups with pagination."""
    groups, _ = await service.list(skip=skip, limit=min(limit, 100))
    return groups


@router.get("/{id}", response_model=MovementGroupResponse)
async def get_movement_group(
    id: UUID, 
    service: MovementGroupService = Depends(get_movement_group_service)
):
    """Get movement group by ID."""
    result = await service.get_by_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement group not found")
    return result


@router.patch("/{id}", response_model=MovementGroupResponse)
async def update_movement_group(
    id: UUID, 
    in_data: dict, 
    service: MovementGroupService = Depends(get_movement_group_service)
):
    """Update movement group by ID."""
    result = await service.update(id=id, in_data=in_data)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement group not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movement_group(
    id: UUID, 
    service: MovementGroupService = Depends(get_movement_group_service)
):
    """Soft delete movement group."""
    if not await service.delete(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movement group not found")
    return None
