import pytest
from httpx import AsyncClient


class TestMuscleGroups:
    prefix = "/api/v1/admin/catalog/muscle-groups"

    async def test_create(self, client: AsyncClient, sample_muscle_group: dict):
        resp = await client.post(f"{self.prefix}/", json=sample_muscle_group)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == sample_muscle_group["name"]
        assert "id" in data

    async def test_list(self, client: AsyncClient, sample_muscle_group: dict):
        await client.post(f"{self.prefix}/", json=sample_muscle_group)
        resp = await client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1

    async def test_get_by_id(self, client: AsyncClient, sample_muscle_group: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_muscle_group)).json()
        resp = await client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_get_not_found(self, client: AsyncClient):
        resp = await client.get(f"{self.prefix}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    async def test_update(self, client: AsyncClient, sample_muscle_group: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_muscle_group)).json()
        resp = await client.patch(f"{self.prefix}/{created['id']}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    async def test_delete(self, client: AsyncClient, sample_muscle_group: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_muscle_group)).json()
        resp = await client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204
        get_resp = await client.get(f"{self.prefix}/{created['id']}")
        assert get_resp.status_code == 404


class TestMovementGroups:
    prefix = "/api/v1/admin/catalog/movement-groups"

    async def test_create(self, client: AsyncClient, sample_movement_group: dict):
        resp = await client.post(f"{self.prefix}/", json=sample_movement_group)
        assert resp.status_code == 201
        assert resp.json()["name"] == sample_movement_group["name"]

    async def test_list(self, client: AsyncClient, sample_movement_group: dict):
        await client.post(f"{self.prefix}/", json=sample_movement_group)
        resp = await client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_get_by_id(self, client: AsyncClient, sample_movement_group: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_movement_group)).json()
        resp = await client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_update(self, client: AsyncClient, sample_movement_group: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_movement_group)).json()
        resp = await client.patch(f"{self.prefix}/{created['id']}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    async def test_delete(self, client: AsyncClient, sample_movement_group: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_movement_group)).json()
        resp = await client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204


class TestEquipment:
    prefix = "/api/v1/admin/catalog/equipment"

    async def test_create(self, client: AsyncClient, sample_equipment: dict):
        resp = await client.post(f"{self.prefix}/", json=sample_equipment)
        assert resp.status_code == 201
        assert resp.json()["name"] == sample_equipment["name"]

    async def test_list(self, client: AsyncClient, sample_equipment: dict):
        await client.post(f"{self.prefix}/", json=sample_equipment)
        resp = await client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_get_by_id(self, client: AsyncClient, sample_equipment: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_equipment)).json()
        resp = await client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_update(self, client: AsyncClient, sample_equipment: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_equipment)).json()
        resp = await client.patch(f"{self.prefix}/{created['id']}", json={"name": "Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    async def test_delete(self, client: AsyncClient, sample_equipment: dict):
        created = (await client.post(f"{self.prefix}/", json=sample_equipment)).json()
        resp = await client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204


class TestExercises:
    prefix = "/api/v1/admin/catalog/exercises"

    async def _create_prerequisites(self, client: AsyncClient, tag: str) -> tuple:
        mg = (await client.post("/api/v1/admin/catalog/muscle-groups/", json={
            "name": f"MG-{tag}", "slug": f"mg-{tag}",
        })).json()
        mvg = (await client.post("/api/v1/admin/catalog/movement-groups/", json={
            "name": f"MVG-{tag}", "slug": f"mvg-{tag}",
        })).json()
        return mg["id"], mvg["id"]

    async def test_create(self, client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(client, tag)
        resp = await client.post(f"{self.prefix}/", json={
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

    async def test_list(self, client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(client, tag)
        await client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })
        resp = await client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    async def test_get_by_id(self, client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(client, tag)
        created = (await client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })).json()
        resp = await client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    async def test_update(self, client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(client, tag)
        created = (await client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })).json()
        resp = await client.patch(f"{self.prefix}/{created['id']}", json={"name": "Supino Inclinado"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Supino Inclinado"

    async def test_delete(self, client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        muscle_id, movement_id = await self._create_prerequisites(client, tag)
        created = (await client.post(f"{self.prefix}/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })).json()
        resp = await client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204

    async def test_get_not_found(self, client: AsyncClient):
        resp = await client.get(f"{self.prefix}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404
