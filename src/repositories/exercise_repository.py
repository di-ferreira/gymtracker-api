import re
from uuid import UUID
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, asc, desc
from src.models.exercise import Exercise


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9\s-]", "", name.lower()).replace(" ", "-").strip("-")


class ExerciseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, in_data: dict) -> Exercise:
        if "slug" not in in_data or not in_data.get("slug"):
            in_data["slug"] = _slugify(in_data.get("name", ""))
        db_obj = Exercise(**in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> Exercise | None:
        result = await self.session.execute(
            select(Exercise).where(Exercise.id == id)
        )
        return result.scalar_one_or_none()

    async def update(self, id: UUID, in_data: dict) -> Exercise | None:
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
        db_obj.deleted_at = datetime.utcnow()
        await self.session.commit()
        return True

    async def list_exercises(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Dict[str, Any] = None,
        order_by: str = "name",
        order_dir: str = "asc",
    ) -> tuple[list[Exercise], int]:
        query = select(Exercise)

        if filters:
            if filters.get("name"):
                query = query.where(Exercise.name.ilike(f"%{filters['name']}%"))
            if filters.get("slug"):
                query = query.where(Exercise.slug == filters["slug"])
            if filters.get("difficulty"):
                query = query.where(Exercise.difficulty == filters["difficulty"])
            if filters.get("muscle_group_ids"):
                query = query.where(Exercise.muscle_group_id.in_(filters["muscle_group_ids"]))
            if filters.get("movement_group_ids"):
                query = query.where(Exercise.movement_group_id.in_(filters["movement_group_ids"]))
            if filters.get("search"):
                search_term = f"%{filters['search']}%"
                query = query.where(
                    Exercise.name.ilike(search_term) | Exercise.slug.ilike(search_term)
                )

        order_column = getattr(Exercise, order_by, Exercise.name)
        order_fn = desc if order_dir.lower() == "desc" else asc
        query = query.order_by(order_fn(order_column))

        total_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(total_query)
        total = total_result.scalar() or 0

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        exercises = list(result.scalars().unique().all())

        return exercises, total

    async def search_exercises(
        self, query_str: str, limit: int = 50, order_by: str = "name"
    ) -> tuple[list[Exercise], int]:
        search_term = f"%{query_str}%"
        query = (
            select(Exercise)
            .where(Exercise.name.ilike(search_term) | Exercise.slug.ilike(search_term))
            .order_by(asc(getattr(Exercise, order_by, Exercise.name)))
            .limit(limit)
        )
        result = await self.session.execute(query)
        exercises = list(result.scalars().unique().all())
        return exercises, len(exercises)

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Exercise]:
        result = await self.session.execute(
            select(Exercise).offset(skip).limit(limit)
        )
        return list(result.scalars().unique().all())

    async def delete_equipment(self, exercise_id: UUID, equipment_id: UUID) -> bool:
        from src.models.exercise import ExerciseEquipment
        result = await self.session.execute(
            select(ExerciseEquipment).where(
                ExerciseEquipment.exercise_id == exercise_id,
                ExerciseEquipment.equipment_id == equipment_id,
            )
        )
        rel = result.scalar_one_or_none()
        if not rel:
            return False
        await self.session.delete(rel)
        await self.session.commit()
        return True

    async def add_equipment(
        self, exercise_id: UUID, equipment_id: UUID, usage_note: Optional[str] = None
    ) -> Optional[UUID]:
        from src.models.exercise import ExerciseEquipment
        rel = ExerciseEquipment(
            exercise_id=exercise_id,
            equipment_id=equipment_id,
            usage_note=usage_note,
        )
        self.session.add(rel)
        await self.session.commit()
        return equipment_id
