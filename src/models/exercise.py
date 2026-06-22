import uuid
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Integer, Boolean,
    UniqueConstraint, Index, func, text
)
from sqlalchemy import Uuid
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database.base import Base


class TimestampMixin:
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    deleted_at = Column(
        DateTime,
        nullable=True,
        default=None,
    )


class DifficultyLevel(str, enum.Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class MediaUrlType(str, enum.Enum):
    THUMBNAIL = "THUMBNAIL"
    IMAGE = "IMAGE"
    GIF = "GIF"
    VIDEO = "VIDEO"


class MuscleGroup(Base, TimestampMixin):
    __tablename__ = "muscle_groups"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = Column(
        String(150), nullable=False, index=True, unique=True,
    )

    slug: Mapped[str] = Column(
        String(100), unique=True, nullable=False, index=True,
    )

    description: Mapped[Optional[str]] = Column(Text, nullable=True)

    order_index: Mapped[int] = Column(Integer, default=0, index=True)

    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise", back_populates="muscle_group",
        cascade="all, delete-orphan",
        foreign_keys="Exercise.muscle_group_id"
    )

    __table_args__ = (
        Index("idx_muscle_groups_slug", "slug"),
        Index("idx_muscle_groups_order", "order_index"),
    )


class MovementGroup(Base, TimestampMixin):
    __tablename__ = "movement_groups"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = Column(
        String(150), nullable=False, index=True, unique=True,
    )

    slug: Mapped[str] = Column(
        String(100), unique=True, nullable=False, index=True,
    )

    description: Mapped[Optional[str]] = Column(Text, nullable=True)

    order_index: Mapped[int] = Column(Integer, default=0, index=True)

    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise", back_populates="movement_group",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_movement_groups_slug", "slug"),
        Index("idx_movement_groups_order", "order_index"),
    )


class Equipment(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "equipments"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = Column(
        String(100), nullable=False, index=True, unique=True,
    )

    slug: Mapped[str] = Column(
        String(100), unique=True, nullable=False, index=True,
    )

    description: Mapped[Optional[str]] = Column(Text, nullable=True)

    category: Mapped[Optional[str]] = Column(String(50), nullable=True)

    order_index: Mapped[int] = Column(Integer, default=0)

    __table_args__ = (
        Index("idx_equipments_slug", "slug"),
    )


class Exercise(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = Column(
        String(255), nullable=False, index=True,
    )

    slug: Mapped[str] = Column(
        String(255), unique=True, nullable=False, index=True,
    )

    description: Mapped[Optional[str]] = Column(Text)

    execution_tips: Mapped[Optional[str]] = Column(Text)

    difficulty: Mapped[Optional[str]] = Column(String(20), nullable=True)

    target_muscle_primary: Mapped[Optional[str]] = Column(
        String(100), nullable=True,
    )

    thumbnail_url: Mapped[Optional[str]] = Column(Text)

    image_url: Mapped[Optional[str]] = Column(Text, nullable=True)

    gif_url: Mapped[Optional[str]] = Column(Text, nullable=True)

    video_url: Mapped[Optional[str]] = Column(Text, nullable=True)

    movement_group_id: Mapped[uuid.UUID] = Column(
        Uuid(),
        ForeignKey("movement_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    muscle_group_id: Mapped[uuid.UUID] = Column(
        Uuid(),
        ForeignKey("muscle_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    movement_group: Mapped["MovementGroup"] = relationship(
        "MovementGroup", back_populates="exercises", lazy="joined"
    )

    muscle_group: Mapped["MuscleGroup"] = relationship(
        "MuscleGroup", back_populates="exercises", lazy="joined"
    )

    equipment_relations: Mapped[list["ExerciseEquipment"]] = relationship(
        "ExerciseEquipment", foreign_keys="ExerciseEquipment.exercise_id",
        back_populates="exercise", cascade="all, delete-orphan",
        lazy="selectin"
    )

    instructions: Mapped[list["ExerciseInstruction"]] = relationship(
        "ExerciseInstruction", order_by="ExerciseInstruction.step_order",
        foreign_keys="ExerciseInstruction.exercise_id",
        back_populates="exercise", cascade="all, delete-orphan",
        lazy="selectin"
    )

    alternatives: Mapped[list["ExerciseAlternative"]] = relationship(
        "ExerciseAlternative", foreign_keys="ExerciseAlternative.exercise_id",
        back_populates="exercise_primary",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    __table_args__ = (
        UniqueConstraint("slug", name="uix_exercises_slug"),
        Index("idx_exercises_name", "name"),
        Index("idx_exercises_muscle_group_id", "muscle_group_id"),
        Index("idx_exercises_movement_group_id", "movement_group_id"),
    )


class ExerciseEquipment(Base):
    __tablename__ = "exercise_equipments"

    exercise_id: Mapped[uuid.UUID] = Column(
        Uuid(),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
    )

    equipment_id: Mapped[uuid.UUID] = Column(
        Uuid(),
        ForeignKey("equipments.id", ondelete="CASCADE"),
        primary_key=True,
    )

    usage_note: Mapped[Optional[str]] = Column(Text, nullable=True)

    exercise: Mapped["Exercise"] = relationship(
        "Exercise", back_populates="equipment_relations"
    )


class ExerciseInstruction(Base, TimestampMixin):
    __tablename__ = "exercise_instructions"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    exercise_id: Mapped[uuid.UUID] = Column(
        Uuid(),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    step_order: Mapped[int] = Column(
        Integer, nullable=False, default=0, index=True,
    )

    description: Mapped[str] = Column(Text, nullable=False)

    image_url: Mapped[Optional[str]] = Column(Text, nullable=True)

    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="instructions")

    __table_args__ = (
        Index("idx_instructions_step_order", "exercise_id", "step_order"),
    )


class ExerciseAlternative(Base, TimestampMixin):
    __tablename__ = "exercise_alternatives"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    exercise_id: Mapped[uuid.UUID] = Column(
        Uuid(),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    alternative_exercise_id: Mapped[uuid.UUID] = Column(
        Uuid(),
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    reason: Mapped[Optional[str]] = Column(Text, nullable=True)

    note: Mapped[Optional[str]] = Column(Text, nullable=True)

    exercise_primary: Mapped["Exercise"] = relationship(
        "Exercise", foreign_keys=[exercise_id]
    )

    __table_args__ = (
        Index("idx_alternatives_exercise_id", "exercise_id"),
        Index("idx_alternatives_alt_exercise_id", "alternative_exercise_id"),
    )


class CatalogVersion(Base, TimestampMixin):
    __tablename__ = "catalog_versions"

    id: Mapped[uuid.UUID] = Column(
        Uuid(), primary_key=True, default=uuid.uuid4
    )

    version_major: Mapped[int] = Column(
        Integer, nullable=False, default=1,
    )

    version_minor: Mapped[int] = Column(
        Integer, nullable=False, default=0,
    )

    checksum: Mapped[str] = Column(
        String(64), nullable=False, unique=True, index=True,
    )

    status: Mapped[str] = Column(
        String(20), nullable=False, default="active",
    )

    description: Mapped[Optional[str]] = Column(Text, nullable=True)

    checksum_algorithm: Mapped[str] = Column(
        String(10), default="SHA256",
    )

    sync_metadata: Mapped[Optional[str]] = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("version_major", "version_minor", name="uq_catalog_version"),
        Index("idx_versions_checksum", "checksum", unique=True),
        Index("idx_versions_status", "status"),
    )
