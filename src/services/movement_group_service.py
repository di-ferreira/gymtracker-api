"""Service layer for Movement Group operations."""

from uuid import UUID  
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.movement_group_repository import MovementGroupRepository
from src.models.exercise import MovementGroup
from src.schemas.catalog import MovementGroupCreate, MovementGroupUpdate


class MovementGroupService:
    """Business logic layer for Muscle Groups."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = MovementGroupRepository(session)

    async def create(self, in_data: dict):
        """Create a new movement group."""
        db_obj = MovementGroup(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        # Note: In production, use proper model validation
        return db_obj

    async def get_by_id(self, id: UUID):
        """Get movement group by ID."""
        result = await self.repository.get_by_id(id)
        return result

    async def list(self, skip: int = 0, limit: int = 100) -> List[MovementGroup]:
        """List movement groups with pagination."""
        results = await self.repository.list_all(skip=skip, limit=min(limit, 100))
        return results if results else []

    async def update(self, id: UUID, in_data: dict) -> MovementGroup | None:
        """Update movement group by ID."""
        db_obj = await self.repository.update(id=id, in_data=in_data)
        return db_obj

    async def delete(self, id: UUID) -> bool:
        """Soft delete movement group."""
        return await self.repository.delete(id=id)
