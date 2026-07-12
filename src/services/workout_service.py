from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.workout import Workout, WorkoutExercise
from src.schemas.workout import (
    WorkoutCreate, WorkoutUpdate, WorkoutResponse,
    WorkoutExerciseCreate, WorkoutExerciseUpdate, WorkoutExerciseResponse,
)
from src.schemas.exercise import PaginationInfo
from src.repositories.workout_repository import WorkoutRepository


class WorkoutService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = WorkoutRepository(session)

    async def create(self, user_id: UUID, in_data: WorkoutCreate) -> WorkoutResponse:
        db_obj = await self.repository.create(user_id, in_data.model_dump(exclude={"user_id"}))
        return WorkoutResponse.model_validate(db_obj)

    async def get_by_id(self, id: UUID, user_id: UUID, is_admin: bool = False) -> Optional[WorkoutResponse]:
        db_obj = await self.repository.get_by_id(id)
        if not db_obj:
            return None
        if not is_admin and db_obj.user_id != user_id:
            return None
        return WorkoutResponse.model_validate(db_obj)

    async def list_by_user(
        self, user_id: UUID | None, skip: int = 0, limit: int = 100
    ) -> tuple[List[WorkoutResponse], "PaginationInfo"]:
        workouts, total = await self.repository.list_by_user(user_id, skip, limit)
        total_pages = (total + limit - 1) // limit

        pagination_info = PaginationInfo(
            page=(skip // limit) + 1,
            per_page=limit,
            total_pages=total_pages,
            has_previous=(skip > 0),
            has_next=(total_pages > ((skip // limit) + 1)),
            total_items=total,
        )

        return [WorkoutResponse.model_validate(w) for w in workouts], pagination_info

    async def update(
        self, id: UUID, user_id: UUID, in_data: WorkoutUpdate, is_admin: bool = False
    ) -> Optional[WorkoutResponse]:
        db_obj = await self.repository.update(
            id, user_id, in_data.model_dump(exclude_unset=True), is_admin=is_admin
        )
        return WorkoutResponse.model_validate(db_obj) if db_obj else None

    async def delete(self, id: UUID, user_id: UUID, is_admin: bool = False) -> bool:
        return await self.repository.delete(id, user_id, is_admin=is_admin)

    async def add_exercise(
        self, workout_id: UUID, user_id: UUID, in_data: WorkoutExerciseCreate, is_admin: bool = False
    ) -> Optional[WorkoutExerciseResponse]:
        db_obj = await self.repository.add_exercise(
            workout_id, user_id, in_data.model_dump(), is_admin=is_admin
        )
        return WorkoutExerciseResponse.model_validate(db_obj) if db_obj else None

    async def update_exercise(
        self, exercise_id: UUID, workout_id: UUID, user_id: UUID,
        in_data: WorkoutExerciseUpdate, is_admin: bool = False,
    ) -> Optional[WorkoutExerciseResponse]:
        db_obj = await self.repository.update_exercise(
            exercise_id, workout_id, user_id,
            in_data.model_dump(exclude_unset=True), is_admin=is_admin,
        )
        return WorkoutExerciseResponse.model_validate(db_obj) if db_obj else None

    async def remove_exercise(
        self, exercise_id: UUID, workout_id: UUID, user_id: UUID, is_admin: bool = False
    ) -> bool:
        return await self.repository.remove_exercise(
            exercise_id, workout_id, user_id, is_admin=is_admin
        )

    async def reorder_exercises(
        self, workout_id: UUID, user_id: UUID, exercise_ids: List[UUID], is_admin: bool = False
    ) -> bool:
        return await self.repository.reorder_exercises(
            workout_id, user_id, exercise_ids, is_admin=is_admin
        )
