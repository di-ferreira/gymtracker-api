import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Integer, Float,
    UniqueConstraint, Index, func,
)
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.base import Base
from src.models.exercise import TimestampMixin


class Workout(Base, TimestampMixin):
    __tablename__ = "workouts"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = Column(
        Uuid(), ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    name: Mapped[str] = Column(
        String(255), nullable=False,
    )

    notes: Mapped[Optional[str]] = Column(Text, nullable=True)

    user: Mapped["User"] = relationship("User")

    exercises: Mapped[list["WorkoutExercise"]] = relationship(
        "WorkoutExercise", back_populates="workout",
        cascade="all, delete-orphan",
        order_by="WorkoutExercise.sort_order",
        lazy="selectin",
    )

    __table_args__ = (
        Index("idx_workouts_user_id", "user_id"),
    )


class WorkoutExercise(Base, TimestampMixin):
    __tablename__ = "workout_exercises"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    workout_id: Mapped[uuid.UUID] = Column(
        Uuid(), ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    exercise_id: Mapped[uuid.UUID] = Column(
        Uuid(), ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )

    sort_order: Mapped[int] = Column(
        Integer, nullable=False, default=0,
    )

    sets: Mapped[Optional[int]] = Column(Integer, nullable=True)

    reps: Mapped[Optional[int]] = Column(Integer, nullable=True)

    weight: Mapped[Optional[float]] = Column(Float, nullable=True)

    notes: Mapped[Optional[str]] = Column(Text, nullable=True)

    workout: Mapped["Workout"] = relationship(
        "Workout", back_populates="exercises"
    )

    exercise: Mapped["Exercise"] = relationship("Exercise", lazy="joined")

    __table_args__ = (
        Index("idx_workout_exercises_workout_id", "workout_id"),
        Index("idx_workout_exercises_exercise_id", "exercise_id"),
        UniqueConstraint(
            "workout_id", "exercise_id", "sort_order",
            name="uq_workout_exercise_order",
        ),
    )
