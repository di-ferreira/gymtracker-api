from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.exercise import ExerciseInstruction


class InstructionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, exercise_id: UUID, data: dict) -> ExerciseInstruction:
        obj = ExerciseInstruction(exercise_id=exercise_id, **data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, id: UUID) -> ExerciseInstruction | None:
        result = await self.session.execute(
            select(ExerciseInstruction).filter(ExerciseInstruction.id == id)
        )
        return result.scalar_one_or_none()

    async def list_by_exercise(
        self, exercise_id: UUID
    ) -> list[ExerciseInstruction]:
        result = await self.session.execute(
            select(ExerciseInstruction)
            .filter(ExerciseInstruction.exercise_id == exercise_id)
            .order_by(ExerciseInstruction.step_order)
        )
        return list(result.scalars().all())

    async def update(
        self, id: UUID, data: dict
    ) -> ExerciseInstruction | None:
        obj = await self.get_by_id(id)
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: UUID) -> bool:
        obj = await self.get_by_id(id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
