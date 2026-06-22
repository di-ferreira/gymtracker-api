"""Repository layer for Equipment operations."""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import Equipment


class EquipmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> Equipment:
        """Create new equipment."""
        db_obj = Equipment(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> Equipment | None:
        result = await self.session.execute(
            select(Equipment).where(Equipment.id == id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[Equipment]:
        result = await self.session.execute(
            select(Equipment).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, id: UUID, in_data: dict):
        """Update equipment by ID."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID) -> bool:
        """Soft delete equipment."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        
        from datetime import datetime
        db_obj.deleted_at = datetime.utcnow()
        await self.session.commit()
        return True
