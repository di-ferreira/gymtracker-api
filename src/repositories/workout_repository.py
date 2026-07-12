from uuid import UUID
from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, asc, delete
from src.models.workout import Workout, WorkoutExercise


class WorkoutRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, in_data: dict) -> Workout:
        db_obj = Workout(user_id=user_id, **in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: UUID) -> Workout | None:
        result = await self.session.execute(
            select(Workout).where(Workout.id == id)
        )
        return result.scalar_one_or_none()

    async def list_by_user(
        self, user_id: UUID | None, skip: int = 0, limit: int = 100
    ) -> tuple[List[Workout], int]:
        query = select(Workout).order_by(Workout.created_at.desc())
        if user_id is not None:
            query = query.where(Workout.user_id == user_id)

        total_query = select(func.count()).select_from(query.subquery())
        total_result = await self.session.execute(total_query)
        total = total_result.scalar() or 0

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        workouts = list(result.scalars().unique().all())

        return workouts, total

    async def update(self, id: UUID, user_id: UUID, in_data: dict, is_admin: bool = False) -> Workout | None:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None
        if not is_admin and db_obj.user_id != user_id:
            return None
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: UUID, user_id: UUID, is_admin: bool = False) -> bool:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return False
        if not is_admin and db_obj.user_id != user_id:
            return False
        await self.session.delete(db_obj)
        await self.session.commit()
        return True

    async def add_exercise(
        self, workout_id: UUID, user_id: UUID, in_data: dict, is_admin: bool = False
    ) -> WorkoutExercise | None:
        workout = await self.get_by_id(workout_id)
        if not workout:
            return None
        if not is_admin and workout.user_id != user_id:
            return None
        db_obj = WorkoutExercise(workout_id=workout_id, **in_data)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update_exercise(
        self, exercise_id: UUID, workout_id: UUID, user_id: UUID, in_data: dict, is_admin: bool = False
    ) -> WorkoutExercise | None:
        workout = await self.get_by_id(workout_id)
        if not workout:
            return None
        if not is_admin and workout.user_id != user_id:
            return None
        result = await self.session.execute(
            select(WorkoutExercise).where(
                WorkoutExercise.id == exercise_id,
                WorkoutExercise.workout_id == workout_id,
            )
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return None
        for key, value in in_data.items():
            setattr(db_obj, key, value)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def remove_exercise(
        self, exercise_id: UUID, workout_id: UUID, user_id: UUID, is_admin: bool = False
    ) -> bool:
        workout = await self.get_by_id(workout_id)
        if not workout:
            return False
        if not is_admin and workout.user_id != user_id:
            return False
        result = await self.session.execute(
            select(WorkoutExercise).where(
                WorkoutExercise.id == exercise_id,
                WorkoutExercise.workout_id == workout_id,
            )
        )
        db_obj = result.scalar_one_or_none()
        if not db_obj:
            return False
        await self.session.delete(db_obj)
        await self.session.commit()
        await self.session.refresh(workout)
        return True

    async def reorder_exercises(
        self, workout_id: UUID, user_id: UUID, exercise_ids: List[UUID], is_admin: bool = False
    ) -> bool:
        workout = await self.get_by_id(workout_id)
        if not workout:
            return False
        if not is_admin and workout.user_id != user_id:
            return False
        for i, we_id in enumerate(exercise_ids):
            result = await self.session.execute(
                select(WorkoutExercise).where(
                    WorkoutExercise.id == we_id,
                    WorkoutExercise.workout_id == workout_id,
                )
            )
            db_obj = result.scalar_one_or_none()
            if db_obj:
                db_obj.sort_order = i
        await self.session.commit()
        return True
