from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.instruction_repository import InstructionRepository
from src.repositories.exercise_repository import ExerciseRepository
from src.schemas.instruction import InstructionCreate, InstructionUpdate, InstructionResponse


class InstructionService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = InstructionRepository(session)
        self.exercise_repo = ExerciseRepository(session)

    async def create(
        self, exercise_id: UUID, in_data: InstructionCreate
    ) -> InstructionResponse:
        exercise = await self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        obj = await self.repository.create(
            exercise_id=exercise_id,
            data=in_data.model_dump(),
        )
        return InstructionResponse.model_validate(obj)

    async def list_by_exercise(
        self, exercise_id: UUID
    ) -> List[InstructionResponse]:
        exercise = await self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Exercise not found")

        objs = await self.repository.list_by_exercise(exercise_id)
        return [InstructionResponse.model_validate(o) for o in objs]

    async def update(
        self, instruction_id: UUID, in_data: InstructionUpdate
    ) -> Optional[InstructionResponse]:
        obj = await self.repository.update(
            instruction_id,
            in_data.model_dump(exclude_unset=True),
        )
        return InstructionResponse.model_validate(obj) if obj else None

    async def delete(self, instruction_id: UUID) -> bool:
        return await self.repository.delete(instruction_id)
