import pytest
import pytest_asyncio
import bcrypt
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


class TestMuscleGroups:
    prefix = "/api/v1/admin/catalog/muscle-groups"

    async def test_create(self, auth_client: AsyncClient, sample_muscle_group: dict):
        resp = await auth_client.post(f"{self.prefix}/", json=sample_muscle_group)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == sample_muscle_group["name"]
        assert "id" in data

    async def test_list(self, auth_client: AsyncClient, sample_muscle_group: dict):
        await auth_client.post(f"{self.prefix}/", json=sample_muscle_group)
        resp = await auth_client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

    async def test_get_by_id(self, auth_client: AsyncClient, sample_muscle_group: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_muscle_group)).json()
        resp = await auth_client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_get_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.get(f"{self.prefix}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    async def test_update(self, auth_client: AsyncClient, sample_muscle_group: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_muscle_group)).json()
        resp = await auth_client.patch(f"{self.prefix}/{created['id']}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    async def test_delete(self, auth_client: AsyncClient, sample_muscle_group: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_muscle_group)).json()
        resp = await auth_client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204
        get_resp = await auth_client.get(f"{self.prefix}/{created['id']}")
        assert get_resp.status_code == 404


class TestMovementGroups:
    prefix = "/api/v1/admin/catalog/movement-groups"

    async def test_create(self, auth_client: AsyncClient, sample_movement_group: dict):
        resp = await auth_client.post(f"{self.prefix}/", json=sample_movement_group)
        assert resp.status_code == 201
        assert resp.json()["name"] == sample_movement_group["name"]

    async def test_list(self, auth_client: AsyncClient, sample_movement_group: dict):
        await auth_client.post(f"{self.prefix}/", json=sample_movement_group)
        resp = await auth_client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_get_by_id(self, auth_client: AsyncClient, sample_movement_group: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_movement_group)).json()
        resp = await auth_client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_update(self, auth_client: AsyncClient, sample_movement_group: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_movement_group)).json()
        resp = await auth_client.patch(f"{self.prefix}/{created['id']}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    async def test_delete(self, auth_client: AsyncClient, sample_movement_group: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_movement_group)).json()
        resp = await auth_client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204


class TestEquipment:
    prefix = "/api/v1/admin/catalog/equipment"

    async def test_create(self, auth_client: AsyncClient, sample_equipment: dict):
        resp = await auth_client.post(f"{self.prefix}/", json=sample_equipment)
        assert resp.status_code == 201
        assert resp.json()["name"] == sample_equipment["name"]

    async def test_list(self, auth_client: AsyncClient, sample_equipment: dict):
        await auth_client.post(f"{self.prefix}/", json=sample_equipment)
        resp = await auth_client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_get_by_id(self, auth_client: AsyncClient, sample_equipment: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_equipment)).json()
        resp = await auth_client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_update(self, auth_client: AsyncClient, sample_equipment: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_equipment)).json()
        resp = await auth_client.patch(f"{self.prefix}/{created['id']}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    async def test_delete(self, auth_client: AsyncClient, sample_equipment: dict):
        created = (await auth_client.post(f"{self.prefix}/", json=sample_equipment)).json()
        resp = await auth_client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204


class TestExercises:
    prefix = "/api/v1/admin/catalog/exercises"

    async def _create_prerequisites(self, auth_client: AsyncClient, tag: str) -> tuple:
        mg = (await auth_client.post("/api/v1/admin/catalog/muscle-groups/", json={
            "name": f"MG-{tag}", "slug": f"mg-{tag}",
        })).json()
        mvg = (await auth_client.post("/api/v1/admin/catalog/movement-groups/", json={
            "name": f"MVG-{tag}", "slug": f"mvg-{tag}",
        })).json()
        return mg["id"], mvg["id"]

    async def test_create(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(auth_client, tag)
        resp = await auth_client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "description": "Bench press",
            "difficulty": "Intermediate",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == f"EX-{tag}"
        assert data["slug"] == f"ex-{tag}"

    async def test_list(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(auth_client, tag)
        await auth_client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })
        resp = await auth_client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_get_by_id(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(auth_client, tag)
        created = (await auth_client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })).json()
        resp = await auth_client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_update(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(auth_client, tag)
        created = (await auth_client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })).json()
        resp = await auth_client.patch(f"{self.prefix}/{created['id']}", json={"name": "Supino Inclinado"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Supino Inclinado"

    async def test_delete(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(auth_client, tag)
        created = (await auth_client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })).json()
        resp = await auth_client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204

    async def test_get_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.get(f"{self.prefix}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404


class TestRoleBasedAccess:
    prefix = "/api/v1/admin/catalog/exercises"
    public_prefix = "/api/v1/catalog"

    @pytest_asyncio.fixture
    async def normal_client(self, client: AsyncClient, db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
        from src.models.user import User

        result = await db_session.execute(
            select(User).filter(User.email == "user@test.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="user@test.com",
                hashed_password=bcrypt.hashpw(b"userpass123", bcrypt.gensalt()).decode(),
                name="Test User",
                role="user",
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "user@test.com",
            "password": "userpass123",
        })
        token = login_resp.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
        yield client

    async def test_normal_user_cannot_create_exercise(
        self, normal_client: AsyncClient
    ):
        resp = await normal_client.post(
            f"{self.prefix}/",
            json={"name": "Should Fail", "description": "test"},
        )
        assert resp.status_code == 403

    async def test_normal_user_cannot_update_exercise(
        self, normal_client: AsyncClient
    ):
        resp = await normal_client.patch(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000",
            json={"name": "Should Fail"},
        )
        assert resp.status_code == 403

    async def test_normal_user_cannot_delete_exercise(
        self, normal_client: AsyncClient
    ):
        resp = await normal_client.delete(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000",
        )
        assert resp.status_code == 403

    async def test_public_list_requires_auth(self, client: AsyncClient):
        resp = await client.get(f"{self.public_prefix}/exercises/")
        assert resp.status_code == 401

    async def test_normal_user_can_list_public_exercises(
        self, normal_client: AsyncClient
    ):
        resp = await normal_client.get(f"{self.public_prefix}/exercises/")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
