from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.session import get_db
from src.services.equipment_service import EquipmentService
from src.schemas.catalog import EquipmentCreate, EquipmentUpdate, EquipmentResponse

router = APIRouter(prefix="/equipment", tags=["Equipment"])


async def get_equipment_service(db: AsyncSession = Depends(get_db)):
    return EquipmentService(db)


@router.post("/", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_equipment(in_data: EquipmentCreate, service: EquipmentService = Depends(get_equipment_service)):
    return await service.create(in_data=in_data.model_dump())


@router.get("/", response_model=List[EquipmentResponse])
async def list_equipment(skip: int = 0, limit: int = 100, service: EquipmentService = Depends(get_equipment_service)):
    return await service.list(skip=skip, limit=limit)


@router.get("/{id}", response_model=EquipmentResponse)
async def get_equipment(id: UUID, service: EquipmentService = Depends(get_equipment_service)):
    result = await service.get_by_id(id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    return result


@router.patch("/{id}", response_model=EquipmentResponse)
async def update_equipment(id: UUID, in_data: EquipmentUpdate, service: EquipmentService = Depends(get_equipment_service)):
    result = await service.update(id=id, in_data=in_data.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    return result


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipment(id: UUID, service: EquipmentService = Depends(get_equipment_service)):
    if not await service.delete(id=id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found")
    return None
