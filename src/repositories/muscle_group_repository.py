from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.exercise import MuscleGroup
from src.schemas.muscle_group import MuscleGroupCreate, MuscleGroupUpdate

class MuscleGroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: MuscleGroupCreate) -> MuscleGroup:
        db_obj = MuscleGroup(**data.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> MuscleGroup | None:
        result = await self.session.execute(select(MuscleGroup).filter(MuscleGroup.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[MuscleGroup]:
        result = await self.session.execute(select(MuscleGroup).offset(skip).limit(limit))
        return result.scalars().all()

    async def update(self, id: UUID, data: MuscleGroupUpdate) -> MuscleGroup | None:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
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
