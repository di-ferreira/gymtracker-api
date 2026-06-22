import pytest
import pytest_asyncio
from uuid import uuid4
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from src.database.base import Base
from src.database.session import get_db
from src.main import app


TEST_DATABASE_URL = "sqlite+aiosqlite://"


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    session_factory = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient) -> AsyncGenerator[AsyncClient, None]:
    register_data = {
        "email": "admin@test.com",
        "password": "testpass123",
        "name": "Test Admin",
    }
    resp = await client.post("/api/v1/auth/register", json=register_data)
    if resp.status_code == 409:
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "admin@test.com",
            "password": "testpass123",
        })
        token = login_resp.json()["access_token"]
    else:
        token = (await client.post("/api/v1/auth/login", json={
            "email": "admin@test.com",
            "password": "testpass123",
        })).json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client


@pytest.fixture
def unique_name():
    from uuid import uuid4
    return uuid4().hex[:8]


@pytest.fixture
def sample_muscle_group(unique_name: str):
    return {"name": f"MG-{unique_name}", "slug": f"mg-{unique_name}", "order_index": 1}


@pytest.fixture
def sample_movement_group(unique_name: str):
    return {"name": f"MVG-{unique_name}", "slug": f"mvg-{unique_name}", "order_index": 0}


@pytest.fixture
def sample_equipment(unique_name: str):
    return {"name": f"EQ-{unique_name}", "slug": f"eq-{unique_name}", "category": "free-weight"}


@pytest.fixture
def sample_exercise(unique_name: str):
    return {
        "name": f"EX-{unique_name}",
        "description": "Bench press exercise",
        "difficulty": "Intermediate",
    }
