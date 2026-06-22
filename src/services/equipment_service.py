"""Service layer for Equipment operations."""

from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.repositories.equipment_repository import EquipmentRepository
from src.models.exercise import EquipmentResponse


class EquipmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = EquipmentRepository(session)

    # ==================== CRUD Operations ==================== 

    async def create(self, in_data: dict) -> EquipmentResponse:
        """Create a new equipment type."""
        db_obj = await self.repository.create(in_data=in_data)
        return EquipmentResponse.model_validate(db_obj)

    async def get_by_id(self, id: UUID):
        """Get equipment by ID."""
        db_obj = await self.repository.get_by_id(id)
        return EquipmentResponse.model_validate(db_obj) if db_obj else None

    async def update(self, id: UUID, in_data: dict) -> Optional[EquipmentResponse]:
        """Update equipment by ID."""
        db_obj = await self.repository.update(id=id, in_data=in_data)
        return EquipmentResponse.model_validate(db_obj) if db_obj else None

    async def delete(self, id: UUID) -> bool:
        """Soft delete an equipment (mark as deleted)."""
        return await self.repository.delete(id=id)

    # ==================== List Operations ==================== 

    async def list(self, skip: int = 0, limit: int = 100):
        """List equipment with pagination."""
        equipment_list, total = await self.repository.list(skip=skip, limit=min(limit, 100))
        return equipment_list
