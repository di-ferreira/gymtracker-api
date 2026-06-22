"""Pytest conftest for GymTracker API - Provides test fixtures."""

import pytest
from typing import AsyncGenerator


# ==================== Database Session Fixtures ==================== #

@pytest.fixture(scope="module")
async def async_db_session():
    """Async database session fixture for tests (mock or real DB)."""
    from src.database.session import engine, AsyncSessionLocal
    
    # For testing: use test database or mock
    # In production tests, configure test database in environment
    
    db_session = AsyncSessionLocal()
    try:
        yield db_session
        await db_session.close()
    except Exception as e:
        db_session.rollback()
        await db_session.close()
        raise


# ==================== Model Instances for Testing ==================== #

@pytest.fixture
async def exercise_model(async_db_session):
    """Mock Exercise model instance for tests."""
    from src.models.exercise import Exercise
    from uuid import uuid4
    
    # Create mock instance without committing to DB in unit tests
    return Exercise(
        id=uuid4(),
        name="Supino Mentado",
        slug="supino-mentado",
        movement_group_id=uuid4(),
        muscle_group_id=uuid4(),
        description="Chest exercise targeting pectoral muscles"
    )


@pytest.fixture
async def equipment_model(async_db_session):
    """Mock Equipment model instance for tests."""
    from src.models.exercise import Equipment
    from uuid import uuid4
    
    return Equipment(
        id=uuid4(),
        name="Dumbbell",
        slug="dumbbell"
    )


@pytest.fixture
async def muscle_group_model(async_db_session):
    """Mock MuscleGroup model instance for tests."""
    from src.models.exercise import MuscleGroup
    from uuid import uuid4
    
    return MuscleGroup(
        id=uuid4(),
        name="Peitoral",
        slug="peitoral"
    )


@pytest.fixture  
async def movement_group_model(async_db_session):
    """Mock MovementGroup model instance for tests."""
    from src.models.exercise import MovementGroup
    from uuid import uuid4
    
    return MovementGroup(
        id=uuid4(),
        name="Compound",
        slug="compound"
    )


# ==================== API Client Fixtures ==================== #

@pytest.fixture
async def api_client(base_url: str = "http://testserver"):
    """Async HTTP client for API testing."""
    import httpx
    
    async with httpx.AsyncClient(
        base_url=base_url,
        follow_redirects=False
    ) as client:
        yield client


# ==================== Test Utilities ==================== #

@pytest.fixture
def sample_exercise_data():
    """Sample exercise data for tests."""
    return {
        "name": "Supino Mentado",
        "description": "Chest exercise using dumbbells on an incline bench", 
        "execution_tips": "Keep elbows at 45 degrees, breathe in on up, out on down"
    }


@pytest.fixture
def sample_equipment():
    """Sample equipment data for tests."""
    return {
        "name": "Dumbbell",
        "category": "free-weight",
        "description": "Adjustable or fixed weight dumbbells"
    }


@pytest.fixture
def sample_muscle_group():
    """Sample muscle group data for tests."""
    return {
        "name": "Peitoral",
        "order_index": 1
    }


@pytest.fixture
def sample_movement_group():
    """Sample movement group data for tests."""
    return {
        "name": "Compound",  
        "order_index": 0
    }
