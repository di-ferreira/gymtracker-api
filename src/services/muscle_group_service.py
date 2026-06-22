from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.muscle_group_repository import MuscleGroupRepository
from src.schemas.catalog import MuscleGroupCreate, MuscleGroupUpdate, MuscleGroupResponse


class MuscleGroupService:
    def __init__(self, session: AsyncSession):
        self.repository = MuscleGroupRepository(session)

    async def create_muscle_group(self, data: MuscleGroupCreate) -> MuscleGroupResponse:
        db_obj = await self.repository.create(data)
        return MuscleGroupResponse.model_validate(db_obj)

    async def get_muscle_group(self, id: UUID) -> MuscleGroupResponse | None:
        db_obj = await self.repository.get_by_id(id)
        return MuscleGroupResponse.model_validate(db_obj) if db_obj else None

    async def list_muscle_groups(self, skip: int = 0, limit: int = 100) -> list[MuscleGroupResponse]:
        db_objs = await self.repository.get_all(skip, limit)
        return [MuscleGroupResponse.model_validate(obj) for obj in db_objs]

    async def update_muscle_group(self, id: UUID, data: MuscleGroupUpdate) -> MuscleGroupResponse | None:
        db_obj = await self.repository.update(id, data)
        return MuscleGroupResponse.model_validate(db_obj) if db_obj else None

    async def delete_muscle_group(self, id: UUID) -> bool:
        return await self.repository.delete(id)
