from uuid import UUID
from typing import List, Optional, Dict, Any
from collections import defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.exercise import Exercise, Equipment, ExerciseEquipment
from src.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseResponse, PaginationInfo
from src.schemas.catalog import EquipmentResponse, MuscleGroupResponse, MovementGroupResponse
from src.repositories.exercise_repository import ExerciseRepository


class ExerciseValidationError(Exception):
    pass


class ExerciseService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ExerciseRepository(session)

    async def _load_equipment(self, exercise_id: UUID) -> List[EquipmentResponse]:
        eq_query = await self.session.execute(
            select(Equipment)
            .join(ExerciseEquipment, ExerciseEquipment.equipment_id == Equipment.id)
            .filter(ExerciseEquipment.exercise_id == exercise_id)
        )
        return [EquipmentResponse.model_validate(eq) for eq in eq_query.scalars().all()]

    async def _batch_load_equipment(
        self, exercise_ids: List[UUID]
    ) -> Dict[UUID, List[EquipmentResponse]]:
        if not exercise_ids:
            return {}
        eq_query = await self.session.execute(
            select(Equipment, ExerciseEquipment.exercise_id)
            .join(ExerciseEquipment, ExerciseEquipment.equipment_id == Equipment.id)
            .filter(ExerciseEquipment.exercise_id.in_(exercise_ids))
        )
        result: Dict[UUID, List[EquipmentResponse]] = defaultdict(list)
        for eq, ex_id in eq_query.all():
            result[ex_id].append(EquipmentResponse.model_validate(eq))
        return dict(result)

    async def create(
        self,
        in_data: ExerciseCreate
    ) -> ExerciseResponse:
        db_obj = await self.repository.create(in_data.model_dump())
        result = ExerciseResponse.model_validate(db_obj)
        result.equipment = await self._load_equipment(db_obj.id)
        return result

    async def get_by_id(self, id: UUID) -> Optional[ExerciseResponse]:
        db_obj = await self.repository.get_by_id(id)
        if not db_obj:
            return None
        result = ExerciseResponse.model_validate(db_obj)
        result.equipment = await self._load_equipment(id)
        return result

    async def update(
        self,
        id: UUID,
        in_data: ExerciseUpdate
    ) -> Optional[ExerciseResponse]:
        db_obj = await self.repository.update(id, in_data.model_dump(exclude_unset=True))
        if not db_obj:
            return None
        result = ExerciseResponse.model_validate(db_obj)
        result.equipment = await self._load_equipment(id)
        return result

    async def delete(self, id: UUID) -> bool:
        return await self.repository.delete(id)

    async def list_exercises(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: str = "name",
        order_dir: str = "asc"
    ) -> tuple[List[ExerciseResponse], PaginationInfo]:
        exercises, total = await self.repository.list_exercises(skip, limit, filters, order_by, order_dir)
        total_pages = (total + limit - 1) // limit

        pagination_info = PaginationInfo(
            page=(skip // limit) + 1,
            per_page=limit,
            total_pages=total_pages,
            has_previous=(skip > 0),
            has_next=(total_pages > ((skip // limit) + 1)),
            total_items=total
        )

        exercise_ids = [ex.id for ex in exercises]
        equipment_map = await self._batch_load_equipment(exercise_ids)

        responses = []
        for ex in exercises:
            resp = ExerciseResponse.model_validate(ex)
            resp.equipment = equipment_map.get(ex.id, [])
            responses.append(resp)

        return responses, pagination_info

    async def search_exercises(
        self,
        query: str,
        fuzzy: bool = False,
        limit: int = 50,
        order_by: Optional[str] = None
    ) -> List[ExerciseResponse]:
        exercises, _ = await self.repository.search_exercises(
            query.lower(),
            limit,
            order_by or "name"
        )
        return [ExerciseResponse.model_validate(ex) for ex in exercises]

    async def delete_equipment(self, exercise_id: UUID, equipment_id: UUID) -> bool:
        return await self.repository.delete_equipment(exercise_id, equipment_id)

    async def add_equipment(
        self,
        exercise_id: UUID,
        equipment_id: UUID,
        usage_note: Optional[str] = None
    ) -> Optional[UUID]:
        return await self.repository.add_equipment(
            exercise_id,
            equipment_id,
            usage_note
        )
