from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.repositories.equipment_repository import EquipmentRepository
from src.schemas.catalog import EquipmentResponse


class EquipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = EquipmentRepository(session)

    async def create(self, in_data: dict) -> EquipmentResponse:
        db_obj = await self.repository.create(in_data=in_data)
        return EquipmentResponse.model_validate(db_obj)

    async def get_by_id(self, id: UUID):
        db_obj = await self.repository.get_by_id(id)
        return EquipmentResponse.model_validate(db_obj) if db_obj else None

    async def update(self, id: UUID, in_data: dict) -> Optional[EquipmentResponse]:
        db_obj = await self.repository.update(id=id, in_data=in_data)
        return EquipmentResponse.model_validate(db_obj) if db_obj else None

    async def delete(self, id: UUID) -> bool:
        return await self.repository.delete(id=id)

    async def list(self, skip: int = 0, limit: int = 100):
        equipment_list = await self.repository.list_all(skip=skip, limit=min(limit, 100))
        return [EquipmentResponse.model_validate(eq) for eq in equipment_list]
