"""Script to generate all repository files programmatically."""

import os  
from pathlib import Path

api_root = r"/gymtracker-api"


equipment_repo = '''"""Repository layer for Equipment operations."""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import Equipment


class EquipmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> Equipment:
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
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID) -> bool:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        from datetime import datetime as dt
        db_obj.deleted_at = dt.utcnow()
        await self.session.commit()
        return True
'''

movement_repo = '''"""Repository layer for Movement Group operations."""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import MovementGroup


class MovementGroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> MovementGroup:
        db_obj = MovementGroup(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> MovementGroup | None:
        result = await self.session.execute(
            select(MovementGroup).where(MovementGroup.id == id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[MovementGroup]:
        result = await self.session.execute(
            select(MovementGroup).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, id: UUID, in_data: dict):
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID) -> bool:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        from datetime import datetime as dt
        db_obj.deleted_at = dt.utcnow()
        await self.session.commit()
        return True
'''


muscle_repo = '''"""Repository layer for Muscle Group operations."""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import MuscleGroup


class MuscleGroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> MuscleGroup:
        db_obj = MuscleGroup(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> MuscleGroup | None:
        result = await self.session.execute(
            select(MuscleGroup).where(MuscleGroup.id == id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[MuscleGroup]:
        result = await self.session.execute(
            select(MuscleGroup).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, id: UUID, in_data: dict):
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID) -> bool:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        from datetime import datetime as dt
        db_obj.deleted_at = dt.utcnow()
        await self.session.commit()
        return True
'''


exercise_repo = '''"""Repository layer for Exercise operations."""

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.models.exercise import Expression


class ExerciseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> Expression:
        db_obj = Expression(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> Expression | None:
        result = await self.session.execute(
            select(Expression).where(Expression.id == id)
        )
        return result.scalar_one_or_none()

    async def list_exercises(self, skip: int = 0, limit: int = 100):
        query = select(Expression)
        result = await self.session.execute(
            query.offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, id: UUID, in_data: dict):
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
'''

# Write all files
paths = [
    ("equipment_repository.py", equipment_repo),
    ("movement_group_repository.py", movement_repo),
    ("muscle_group_repository.py", muscle_repo),
    ("exercise_repository.py", exercise_repo),
]

for filepath, content in paths:
    full_path = Path(api_root) / "src" / "repositories" / filepath
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {full_path}")

