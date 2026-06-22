"""
Database models for GymTracker API.
Complete ORM models with UUID v1 IDs, timestamps, soft deletes, and relationships."""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, ForeignKey, Integer, Enum, CheckConstraint, 
    UniqueConstraint, Index, func, event, text
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    
    # Configure table name style (snake_case by default)
    __table_args__ = {"schema": "public"}
    
    def __repr__(self):
        return f"<{self.__tablename__}(id={self.id})>"


class TimestampMixin:
    """Mixin for created_at and updated_at columns."""
    created_at = Column(
        DateTime, 
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp"
    )
    updated_at = Column(
        DateTime, 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update timestamp"
    )


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""
    deleted_at = Column(
        DateTime, 
        nullable=True,
        default=None,
        comment="Soft delete timestamp - use soft delete instead of hard delete"
    )


# Enums for type safety
DifficultyLevel = Enum('Difficulty', 'Beginner Intermediate Advanced Expert', name='difficulty_level')
MediaUrlType = Enum('MediaType', 'THUMBNAIL IMAGE GIF VIDEO', name='media_type')


class MuscleGroup(Base, TimestampMixin):
    """
    Muscle Group model - groups exercises by the muscle area targeted.
    
    Examples: Chest (Peitoral), Back (Costas), Legs (Pernas)
    """
    __tablename__ = "muscle_groups"
    
    # Primary key using UUID v1 for better versioning/traceability
    id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        server_default="gen_random_uuid()",
        comment="UUID v1 with clock sequence for traceability"
    )
    
    name: Mapped[str] = Column(
        String(150), 
        nullable=False, 
        index=True,
        unique=True,
        comment="Display name for muscle group"
    )
    
    slug: Mapped[str] = Column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="URL-safe identifier (e.g., 'peitoral', 'costas')",
        comment="Generated from name - should be lowercase, hyphen-separated"
    )
    
    description: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="Detailed description of the muscle group"
    )
    
    order_index: Mapped[int] = Column(
        Integer, default=0, index=True,
        comment="Display order - used for sorting in UI"
    )
    
    # Relationships
    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise", back_populates="muscle_group", lazy="joined",
        cascade="all, delete-orphan",
        foreign_keys="Exercise.muscle_group_id"
    )
    
    __table_args__ = (
        Index("idx_muscle_groups_slug", "slug"),
        Index("idx_muscle_groups_order", "order_index"),
        CheckConstraint('order_index >= 0', name='muscle_groups_order_check'),
    )


class MovementGroup(Base, TimestampMixin):
    """
    Movement Group model - groups exercises by movement pattern.
    
    Examples: Compound (Multi-Joint), Isolation, Push, Pull
    """
    __tablename__ = "movement_groups"
    
    id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        server_default="gen_random_uuid()",
        comment="UUID v1 for traceability"
    )
    
    name: Mapped[str] = Column(
        String(150), 
        nullable=False, 
        index=True,
        unique=True,
        comment="Display name for movement group"
    )
    
    slug: Mapped[str] = Column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="URL-safe identifier (e.g., 'compound', 'isolation')"
    )
    
    description: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="Description of movement patterns in this group"
    )
    
    order_index: Mapped[int] = Column(
        Integer, default=0, index=True
    )
    
    # Relationships
    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise", back_populates="movement_group", lazy="joined",
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        Index("idx_movement_groups_slug", "slug"),
        Index("idx_movement_groups_order", "order_index"),
    )


class Equipment(Base, TimestampMixin):
    """
    Equipment model - types of equipment used in exercises.
    
    Examples: Dumbbell, Barbell, Cable Machine, Bodyweight
    """
    __tablename__ = "equipments"
    
    id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        server_default="gen_random_uuid()"
    )
    
    name: Mapped[str] = Column(
        String(100), 
        nullable=False, 
        index=True,
        unique=True,
        comment="Display name for equipment type"
    )
    
    slug: Mapped[str] = Column(
        String(100), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="URL-safe identifier (e.g., 'dumbbell', 'barbell')"
    )
    
    description: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="Detailed description of the equipment"
    )
    
    category: Mapped[Optional[str]] = Column(
        String(50), nullable=True,
        comment="Equipment category (e.g., 'free-weight', 'machine', 'accessory')"
    )
    
    order_index: Mapped[int] = Column(Integer, default=0)
    
    __table_args__ = (
        Index("idx_equipments_slug", "slug"),
    )


class Exercise(Base, TimestampMixin, SoftDeleteMixin):
    """
    Exercise model - core exercise definition with rich metadata.
    
    This is the primary table in the catalog containing all exercise details.
    """
    __tablename__ = "exercises"
    
    id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        server_default="gen_random_uuid()"
    )
    
    name: Mapped[str] = Column(
        String(255), 
        nullable=False, 
        index=True,
        comment="Display name for the exercise (e.g., 'Supino Mentado', 'Agachamento')"
    )
    
    slug: Mapped[str] = Column(
        String(255), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="URL-safe identifier"
    )
    
    description: Mapped[Optional[str]] = Column(
        Text,
        comment="Detailed explanation of the exercise and targeting area"
    )
    
    execution_tips: Mapped[Optional[str]] = Column(
        Text,
        comment="Tips for proper execution and common mistakes to avoid"
    )
    
    difficulty: Mapped[Optional[DifficultyLevel]] = Column(
        DifficultyLevel,
        nullable=True,
        comment="Difficulty level of exercise"
    )
    
    target_muscle_primary: Mapped[Optional[str]] = Column(
        String(100), nullable=True,
        comment="Primary muscle group targeted (free-text for flexibility)"
    )
    
    thumbnail_url: Mapped[Optional[str]] = Column(
        Text,  # Using Text to allow any URL length
        comment="URL to thumbnail image or video"
    )
    
    image_url: Mapped[Optional[str]] = Column(
        Text,
        nullable=True,
        comment="URL to main illustration image"
    )
    
    gif_url: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="URL to GIF demonstrating exercise movement"
    )
    
    video_url: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="URL to full exercise demonstration video"
    )
    
    # Relationships - Foreign keys with "orphan" cascade for data integrity
    movement_group_id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("movement_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Link to MovementGroup table (movement pattern)"
    )
    
    muscle_group_id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("muscle_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Link to MuscleGroup table (targeting area)"
    )
    
    movement_group: Mapped["MovementGroup"] = relationship(
        "MovementGroup", back_populates="exercises", lazy="joined"
    )
    
    muscle_group: Mapped["MuscleGroup"] = relationship(
        "MuscleGroup", back_populates="exercises", lazy="joined"
    )
    
    equipment_relations: Mapped[list["ExerciseEquipment"]] = relationship(
        "ExerciseEquipment", foreign_keys="ExerciseEquipment.exercise_id",
        back_populates="exercise", cascade="all, delete-orphan"
    )
    
    instructions: Mapped[list["ExerciseInstruction"]] = relationship(
        "ExerciseInstruction",  order_by=ExerciseInstruction.step_order,
        foreign_keys="ExerciseInstruction.exercise_id",
        back_populates="exercise", cascade="all, delete-orphan"
    )
    
    alternatives: Mapped[list["ExerciseAlternative"]] = relationship(
        "ExerciseAlternative", primary_key="exercise_alternative_id", foreign_keys="ExerciseAlternative.exercise_id",
        back_populates="exercise_primary", 
        cascade="all, delete-orphan"
    )
    
    __table_args__ = (
        UniqueConstraint("slug", name="uix_exercises_slug"),
        Index("idx_exercises_name", "name"),
        Index("idx_exercises_muscle_group_id", "muscle_group_id"),
        Index("idx_exercises_movement_group_id", "movement_group_id"),
        CheckConstraint('difficulty IS NULL OR difficulty IN (\'Beginner\', \'Intermediate\', \'Advanced\', \'Expert\')', name='exercises_difficulty_check'),
    )


class ExerciseEquipment(Base):
    """
    Junction table for exercising-equipment relationship.
    
    Many-to-Many: An exercise can use multiple types of equipment.
    Many-to-Many: A piece of equipment can be used by multiple exercises.
    """
    __tablename__ = "exercise_equipments"
    
    exercise_id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Reference to Exercise table"
    )
    
    equipment_id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("equipments.id", ondelete="CASCADE"),
        primary_key=True,
        comment="Reference to Equipment table"
    )
    
    usage_note: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="How this equipment is used for this exercise (optional)"
    )
    
    exercise: Mapped["Exercise"] = relationship(
        "Exercise", back_populates="equipment_relations"
    )
    
    __table_args__ = ()


class ExerciseInstruction(Base, TimestampMixin):
    """
    Exercise step-by-step instruction model.
    
    Each instruction represents a step in performing the exercise properly.
    Ordered by step_order.
    """
    __tablename__ = "exercise_instructions"
    
    id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        server_default="gen_random_uuid()"
    )
    
    exercise_id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("exercises.id", ondelete="CASCADE"),  # CASCADE so steps delete with exercise
        nullable=False,
        index=True
    )
    
    step_order: Mapped[int] = Column(
        Integer, nullable=False, default=0, index=True,
        comment="Step number - determines display order"
    )
    
    description: Mapped[str] = Column(
        Text, nullable=False,
        comment="Detailed instruction for this step"
    )
    
    image_url: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="Optional image URL for this step"
    )
    
    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="instructions")
    
    __table_args__ = (
        Index("idx_instructions_step_order", "exercise_id", "step_order"),
    )


class ExerciseAlternative(Base, TimestampMixin):
    """
    Exercise alternative model - suggests substitute exercises.
    
    Used for:
    1. When target muscle is sore/injured
    2. When equipment is unavailable  
    3. Similar exercise alternatives
    
    This creates a bidirectional relationship where one exercise can be an 
    alternative to multiple others (many-to-many).
    """
    __tablename__ = "exercise_alternatives"
    
    id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        server_default="gen_random_uuid()"
    )
    
    exercise_id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Exercise for which this is an alternative"
    )
    
    alternative_exercise_id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,  # Composite PK for many-to-many
        index=True,
        comment="Alternative exercise (the substitute)"
    )
    
    reason: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="Why this is an alternative (e.g., 'use when chest is sore')"
    )
    
    note: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="Additional notes about the alternative"
    )
    
    exercise_primary: Mapped["Exercise"] = relationship("Exercise", foreign_keys=[exercise_id])
    # Note: Many-to-many means bidirectional relationships
    
    __table_args__ = (
        Index("idx_alternatives_exercise_id", "exercise_id"),
        Index("idx_alternatives_alt_exercise_id", "alternative_exercise_id"),
    )


class CatalogVersion(Base, TimestampMixin):
    """
    Catalog version tracking model.
    
    Tracks major releases/syncs of the catalog with checksums for integrity verification.
    Used for:
    1. Syncing changes to external systems
    2. Content versioning
    3. Audit trail for API consumers
    """
    __tablename__ = "catalog_versions"
    
    id: Mapped[uuid.UUID] = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        server_default="gen_random_uuid()"
    )
    
    version_major: Mapped[int] = Column(
        Integer, nullable=False, server_default=text("'1'"),
        comment="Major version for breaking changes (e.g., 1 = initial release)"
    )
    
    version_minor: Mapped[int] = Column(
        Integer, nullable=False, server_default=text("'0'"),
        comment="Minor version for additive changes"
    )
    
    checksum: Mapped[str] = Column(
        String(64), 
        nullable=False, 
        unique=True,
        index=True,
        comment="SHA-256 hash of all catalog data for content integrity verification",
        doc="""Calculated as SHA-256(SHA1(exercise) || SHA1(muscle_group) || SHA1(movement_group) etc.)"""
    )
    
    status: Mapped[str] = Column(
        String(20), 
        nullable=False, 
        default="active",
        comment="Version status: active, deprecated, inactive"
    )
    
    description: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        comment="Changelog or description of changes in this version"
    )
    
    checksum_algorithm: Mapped[str] = Column(
        String(10), 
        default="SHA256",
        comment="Hashing algorithm used for checksum (currently SHA-256)"
    )
    
    sync_metadata: Mapped[Optional[str]] = Column(
        Text, nullable=True,
        doc="""JSON metadata: {"synced_from": "source_system", "timestamp": "...", "notes": "..."}"""
    )
    
    __table_args__ = (
        UniqueConstraint("version_major", "version_minor", name="uq_catalog_version"),
        Index("idx_versions_checksum", "checksum", unique=True),
        Index("idx_versions_status", "status"),
    )


# Triggers for automatic slug generation and timestamp updates
# Note: In PostgreSQL, use raw SQL here or in migration scripts
