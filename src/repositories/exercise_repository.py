"""Repository layer for Exercise operations."""

from uuid import UUID
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import Exercise


class ExerciseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> Exercise:
        """Create new exercise."""
        db_obj = Exercise(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> Exercise | None:
        """Get exercise by ID."""
        result = await self.session.execute(
            select(Exercise).where(Exercise.id == id)
        )
        return result.scalar_one_or_none()

    async def list_exercises(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        filters: Dict[str, Any] = None,
        order_by: str = "name",
        order_dir: str = "asc"
    ) -> tuple[list[Exercise], int]:
        """List exercises with pagination and optional filters."""
        query = select(Exercise).order_by(getattr(Exercise, order_dir.lower(), Expression.created_at)) if hasattr(Expression, 'created_at') else 0
        offset = skip if order_direction == "desc" else skip
        total = await self.session.execute(select(func.count()).scalar())
        return [], total
