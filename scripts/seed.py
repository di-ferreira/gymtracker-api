"""Seed script to populate the database with sample data."""
import asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.core.config import settings
from src.database.base import Base
from src.models.exercise import (
    MuscleGroup, MovementGroup, Equipment, Exercise,
    ExerciseEquipment, ExerciseInstruction,
)


def _slugify(name: str) -> str:
    import re
    return re.sub(r"[^a-z0-9\s-]", "", name.lower()).replace(" ", "-").strip("-")


MUSCLE_GROUPS = [
    {"name": "Peitoral", "order_index": 1},
    {"name": "Costas", "order_index": 2},
    {"name": "Ombro", "order_index": 3},
    {"name": "Bíceps", "order_index": 4},
    {"name": "Tríceps", "order_index": 5},
    {"name": "Quadríceps", "order_index": 6},
    {"name": "Posterior", "order_index": 7},
    {"name": "Glúteo", "order_index": 8},
    {"name": "Abdômen", "order_index": 9},
    {"name": "Panturrilha", "order_index": 10},
    {"name": "Trapézio", "order_index": 11},
    {"name": "Antebraço", "order_index": 12},
]

MOVEMENT_GROUPS = [
    {"name": "Composto", "order_index": 0},
    {"name": "Isolamento", "order_index": 1},
    {"name": "Puxada", "order_index": 2},
    {"name": "Empurrada", "order_index": 3},
    {"name": "Agachamento", "order_index": 4},
    {"name": "Articulação", "order_index": 5},
    {"name": "Rotação", "order_index": 6},
    {"name": "Core", "order_index": 7},
]

EQUIPMENT = [
    {"name": "Barra Reta", "category": "bar"},
    {"name": "Barra W", "category": "bar"},
    {"name": "Halteres", "category": "free-weight"},
    {"name": "Kettlebell", "category": "free-weight"},
    {"name": "Máquina", "category": "machine"},
    {"name": "Cabo", "category": "cable"},
    {"name": "Elástico", "category": "accessory"},
    {"name": "Banco", "category": "bench"},
    {"name": "Step", "category": "platform"},
    {"name": "Bola", "category": "accessory"},
    {"name": "Peso Corporal", "category": "bodyweight"},
    {"name": "Anilhas", "category": "plate"},
]

EXERCISES = [
    {"name": "Supino Reto", "muscle": "Peitoral", "movement": "Empurrada", "difficulty": "Intermediate", "equipment": ["Barra Reta", "Halteres"]},
    {"name": "Supino Inclinado", "muscle": "Peitoral", "movement": "Empurrada", "difficulty": "Intermediate", "equipment": ["Barra Reta", "Halteres"]},
    {"name": "Supino Declinado", "muscle": "Peitoral", "movement": "Empurrada", "difficulty": "Intermediate", "equipment": ["Barra Reta", "Halteres"]},
    {"name": "Crucifixo Reto", "muscle": "Peitoral", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres"]},
    {"name": "Crucifixo Inclinado", "muscle": "Peitoral", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres"]},
    {"name": "Cross Over", "muscle": "Peitoral", "movement": "Isolamento", "difficulty": "Intermediate", "equipment": ["Cabo"]},
    {"name": "Puxada Aberta", "muscle": "Costas", "movement": "Puxada", "difficulty": "Beginner", "equipment": ["Máquina", "Cabo"]},
    {"name": "Puxada Fechada", "muscle": "Costas", "movement": "Puxada", "difficulty": "Beginner", "equipment": ["Máquina", "Cabo"]},
    {"name": "Remada Curvada", "muscle": "Costas", "movement": "Puxada", "difficulty": "Intermediate", "equipment": ["Barra Reta", "Halteres"]},
    {"name": "Remada Unilateral", "muscle": "Costas", "movement": "Puxada", "difficulty": "Intermediate", "equipment": ["Halteres"]},
    {"name": "Levantamento Terra", "muscle": "Costas", "movement": "Composto", "difficulty": "Advanced", "equipment": ["Barra Reta", "Anilhas"]},
    {"name": "Desenvolvimento", "muscle": "Ombro", "movement": "Empurrada", "difficulty": "Intermediate", "equipment": ["Barra Reta", "Halteres"]},
    {"name": "Elevação Lateral", "muscle": "Ombro", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres"]},
    {"name": "Elevação Frontal", "muscle": "Ombro", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres", "Cabo"]},
    {"name": "Crucifixo Inverso", "muscle": "Ombro", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres"]},
    {"name": "Encolhimento", "muscle": "Trapézio", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres", "Barra Reta"]},
    {"name": "Rosca Direta", "muscle": "Bíceps", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Barra Reta", "Barra W", "Halteres"]},
    {"name": "Rosca Alternada", "muscle": "Bíceps", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres"]},
    {"name": "Rosca Martelo", "muscle": "Bíceps", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres"]},
    {"name": "Rosca Concentrada", "muscle": "Bíceps", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Halteres"]},
    {"name": "Tríceps Pulley", "muscle": "Tríceps", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Cabo"]},
    {"name": "Tríceps Testa", "muscle": "Tríceps", "movement": "Isolamento", "difficulty": "Intermediate", "equipment": ["Barra W", "Halteres"]},
    {"name": "Mergulho", "muscle": "Tríceps", "movement": "Empurrada", "difficulty": "Intermediate", "equipment": ["Peso Corporal", "Banco"]},
    {"name": "Tríceps Francês", "muscle": "Tríceps", "movement": "Isolamento", "difficulty": "Intermediate", "equipment": ["Halteres"]},
    {"name": "Agachamento Livre", "muscle": "Quadríceps", "movement": "Agachamento", "difficulty": "Intermediate", "equipment": ["Barra Reta", "Peso Corporal"]},
    {"name": "Agachamento Frontal", "muscle": "Quadríceps", "movement": "Agachamento", "difficulty": "Advanced", "equipment": ["Barra Reta"]},
    {"name": "Cadeira Extensora", "muscle": "Quadríceps", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Máquina"]},
    {"name": "Leg Press", "muscle": "Quadríceps", "movement": "Empurrada", "difficulty": "Intermediate", "equipment": ["Máquina"]},
    {"name": "Mesa Flexora", "muscle": "Posterior", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Máquina"]},
    {"name": "Stiff", "muscle": "Posterior", "movement": "Articulação", "difficulty": "Intermediate", "equipment": ["Barra Reta", "Halteres"]},
    {"name": "Cadeira Flexora", "muscle": "Posterior", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Máquina"]},
    {"name": "Elevação Pélvica", "muscle": "Glúteo", "movement": "Empurrada", "difficulty": "Beginner", "equipment": ["Barra Reta", "Peso Corporal"]},
    {"name": "Agachamento Búlgaro", "muscle": "Glúteo", "movement": "Agachamento", "difficulty": "Intermediate", "equipment": ["Halteres"]},
    {"name": "Abdominal Remador", "muscle": "Abdômen", "movement": "Core", "difficulty": "Beginner", "equipment": ["Cabo", "Peso Corporal"]},
    {"name": "Prancha", "muscle": "Abdômen", "movement": "Core", "difficulty": "Beginner", "equipment": ["Peso Corporal"]},
    {"name": "Elevação de Pernas", "muscle": "Abdômen", "movement": "Core", "difficulty": "Intermediate", "equipment": ["Peso Corporal"]},
    {"name": "Gêmeos em Pé", "muscle": "Panturrilha", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Máquina", "Peso Corporal"]},
    {"name": "Gêmeos Sentado", "muscle": "Panturrilha", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Máquina"]},
    {"name": "Rosca Punho", "muscle": "Antebraço", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Barra Reta", "Halteres"]},
    {"name": "Rosca Punho Inversa", "muscle": "Antebraço", "movement": "Isolamento", "difficulty": "Beginner", "equipment": ["Barra Reta"]},
]


async def seed():
    engine = create_async_engine(settings.database_url, echo=False)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        from sqlalchemy import select
        from src.models.user import User
        import bcrypt

        existing_admin = await session.execute(
            select(User).filter(User.email == "admin@gymtracker.com")
        )
        if not existing_admin.scalar_one_or_none():
            admin = User(
                email="admin@gymtracker.com",
                hashed_password=bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode(),
                name="Admin",
                role="admin",
            )
            session.add(admin)

        async def _get_or_create(s_model, lookup_key, defaults):
            slug = _slugify(lookup_key)
            result = await session.execute(select(s_model).filter(s_model.slug == slug))
            existing = result.scalar_one_or_none()
            if existing:
                return existing
            obj = s_model(slug=slug, **defaults)
            session.add(obj)
            return obj

        muscle_map = {}
        for mg in MUSCLE_GROUPS:
            obj = await _get_or_create(MuscleGroup, mg["name"], {
                "name": mg["name"], "order_index": mg["order_index"],
            })
            await session.flush()
            muscle_map[mg["name"]] = obj.id

        movement_map = {}
        for mvg in MOVEMENT_GROUPS:
            obj = await _get_or_create(MovementGroup, mvg["name"], {
                "name": mvg["name"], "order_index": mvg["order_index"],
            })
            await session.flush()
            movement_map[mvg["name"]] = obj.id

        equipment_map = {}
        for eq in EQUIPMENT:
            obj = await _get_or_create(Equipment, eq["name"], {
                "name": eq["name"], "category": eq["category"],
            })
            await session.flush()
            equipment_map[eq["name"]] = obj.id

        for ex in EXERCISES:
            result = await session.execute(
                select(Exercise).filter(Exercise.slug == _slugify(ex["name"]))
            )
            if result.scalar_one_or_none():
                continue

            exercise = Exercise(
                name=ex["name"],
                slug=_slugify(ex["name"]),
                difficulty=ex["difficulty"],
                muscle_group_id=muscle_map[ex["muscle"]],
                movement_group_id=movement_map[ex["movement"]],
            )
            session.add(exercise)
            await session.flush()

            for eq_name in ex["equipment"]:
                eq_obj = ExerciseEquipment(
                    exercise_id=exercise.id,
                    equipment_id=equipment_map[eq_name],
                )
                session.add(eq_obj)

            if ex["name"] == "Supino Reto":
                instructions = [
                    ExerciseInstruction(
                        exercise_id=exercise.id, step_order=1,
                        description="Deite-se no banco reto com os pés apoiados no chão",
                    ),
                    ExerciseInstruction(
                        exercise_id=exercise.id, step_order=2,
                        description="Segure a barra com as mãos na largura dos ombros",
                    ),
                    ExerciseInstruction(
                        exercise_id=exercise.id, step_order=3,
                        description="Desça a barra até o peito controlando o movimento",
                    ),
                    ExerciseInstruction(
                        exercise_id=exercise.id, step_order=4,
                        description="Empurre a barra para cima até estender os braços",
                    ),
                ]
                session.add_all(instructions)

        await session.commit()

    print("Seed complete!")
    print(f"  {len(MUSCLE_GROUPS)} muscle groups")
    print(f"  {len(MOVEMENT_GROUPS)} movement groups")
    print(f"  {len(EQUIPMENT)} equipment")
    print(f"  {len(EXERCISES)} exercises")


if __name__ == "__main__":
    asyncio.run(seed())
