import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from src.database.base import Base
from src.models.exercise import (
    Exercise, MuscleGroup, MovementGroup, Equipment,
    ExerciseEquipment, ExerciseInstruction, ExerciseAlternative, CatalogVersion,
)
from src.models.user import User
from src.core.config import settings

config = context.config

if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except Exception:
        logging.basicConfig(level=logging.WARN)

target_metadata = Base.metadata


def get_sync_url() -> str:
    url = settings.database_url
    if url.startswith("sqlite+aiosqlite://"):
        url = url.replace("sqlite+aiosqlite://", "sqlite://", 1)
    elif url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
    return url


def run_migrations_online() -> None:
    config.set_main_option("sqlalchemy.url", get_sync_url())
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline() -> None:
    url = get_sync_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
