import re
from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import MovementGroup


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9\s-]", "", name.lower()).replace(" ", "-").strip("-")


class MovementGroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> MovementGroup:
        if "slug" not in in_data or not in_data.get("slug"):
            in_data["slug"] = _slugify(in_data.get("name", ""))
        db_obj = MovementGroup(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID):
        result = await self.session.execute(
            select(MovementGroup).where(MovementGroup.id == id)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100):
        result = await self.session.execute(
            select(MovementGroup).offset(skip).limit(limit)
        )
        return list(result.scalars().unique().all())

    async def update(self, id: UUID, in_data: dict) -> MovementGroup | None:
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

        await self.session.delete(db_obj)
        await self.session.commit()
        return True
