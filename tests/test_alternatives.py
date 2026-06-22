import pytest
from httpx import AsyncClient


class TestAlternatives:
    prefix = "/api/v1/admin/catalog/exercises"

    async def _create_exercise(self, auth_client: AsyncClient, tag: str) -> str:
        mg = (await auth_client.post("/api/v1/admin/catalog/muscle-groups/", json={
            "name": f"MG-{tag}", "slug": f"mg-{tag}",
        })).json()
        mvg = (await auth_client.post("/api/v1/admin/catalog/movement-groups/", json={
            "name": f"MVG-{tag}", "slug": f"mvg-{tag}",
        })).json()
        ex = (await auth_client.post("/api/v1/admin/catalog/exercises/", json={
            "name": f"EX-{tag}",
            "movement_group_id": mvg["id"],
            "muscle_group_id": mg["id"],
        })).json()
        return ex["id"]

    async def test_create_and_list_alternative(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        ex1_id = await self._create_exercise(auth_client, f"{tag}-1")
        ex2_id = await self._create_exercise(auth_client, f"{tag}-2")

        resp = await auth_client.post(
            f"{self.prefix}/{ex1_id}/alternatives/",
            json={"alternative_exercise_id": ex2_id, "reason": "Same muscle group", "note": "Try this instead"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["alternative_exercise_id"] == ex2_id
        assert data["reason"] == "Same muscle group"

        list_resp = await auth_client.get(f"{self.prefix}/{ex1_id}/alternatives/")
        assert list_resp.status_code == 200
        assert len(list_resp.json()) >= 1

    async def test_create_alternative_exercise_not_found(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        ex_id = await self._create_exercise(auth_client, tag)

        resp = await auth_client.post(
            f"{self.prefix}/{ex_id}/alternatives/",
            json={"alternative_exercise_id": "00000000-0000-0000-0000-000000000000"},
        )
        assert resp.status_code == 404

    async def test_list_alternatives_exercise_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.get(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000/alternatives/",
        )
        assert resp.status_code == 404

    async def test_delete_alternative(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        ex1_id = await self._create_exercise(auth_client, f"{tag}-1")
        ex2_id = await self._create_exercise(auth_client, f"{tag}-2")

        created = (await auth_client.post(
            f"{self.prefix}/{ex1_id}/alternatives/",
            json={"alternative_exercise_id": ex2_id},
        )).json()

        resp = await auth_client.delete(
            f"{self.prefix}/{ex1_id}/alternatives/{created['id']}",
        )
        assert resp.status_code == 204

    async def test_delete_alternative_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.delete(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000/alternatives/00000000-0000-0000-0000-000000000000",
        )
        assert resp.status_code == 404
