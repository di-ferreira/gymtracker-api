"""Repository layer for Movement Group operations."""

from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import MovementGroup


class MovementGroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> MovementGroup:
        """Create a new movement group."""
        db_obj = MovementGroup(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID):
        """Get movement group by ID."""
        result = await self.session.execute(
            select(MovementGroup).where(MovementGroup.id == id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100):
        """List all movement groups with pagination."""
        result = await self.session.execute(
            select(MovementGroup).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, id: UUID, in_data: dict) -> MovementGroup | None:
        """Update movement group by ID."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID) -> bool:
        """Delete movement group."""
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        
        await self.session.delete(db_obj)
        await self.session.commit()
        return True
