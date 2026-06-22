from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.alternative_repository import AlternativeRepository
from src.repositories.exercise_repository import ExerciseRepository
from src.schemas.instruction import AlternativeCreate, AlternativeResponse


class AlternativeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = AlternativeRepository(session)
        self.exercise_repo = ExerciseRepository(session)

    async def create(
        self, exercise_id: UUID, in_data: AlternativeCreate
    ) -> AlternativeResponse:
        exercise = await self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        alt_exercise = await self.exercise_repo.get_by_id(
            in_data.alternative_exercise_id
        )
        if not alt_exercise:
            raise ValueError("Alternative exercise not found")

        obj = await self.repository.create(
            exercise_id=exercise_id,
            data=in_data.model_dump(),
        )
        return AlternativeResponse.model_validate(obj)

    async def list_by_exercise(
        self, exercise_id: UUID
    ) -> List[AlternativeResponse]:
        exercise = await self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        objs = await self.repository.list_by_exercise(exercise_id)
        return [AlternativeResponse.model_validate(o) for o in objs]

    async def delete(self, alternative_id: UUID) -> bool:
        return await self.repository.delete(alternative_id)
