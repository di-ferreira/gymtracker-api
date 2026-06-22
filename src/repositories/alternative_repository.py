from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.exercise import ExerciseAlternative


class AlternativeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, exercise_id: UUID, data: dict) -> ExerciseAlternative:
        obj = ExerciseAlternative(exercise_id=exercise_id, **data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, id: UUID) -> ExerciseAlternative | None:
        result = await self.session.execute(
            select(ExerciseAlternative).filter(ExerciseAlternative.id == id)
        )
        return result.scalar_one_or_none()

    async def list_by_exercise(self, exercise_id: UUID) -> list[ExerciseAlternative]:
        result = await self.session.execute(
            select(ExerciseAlternative)
            .filter(ExerciseAlternative.exercise_id == exercise_id)
        )
        return list(result.scalars().all())

    async def delete(self, id: UUID) -> bool:
        obj = await self.get_by_id(id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
