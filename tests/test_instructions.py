import pytest
from httpx import AsyncClient


class TestInstructions:
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

    async def test_create_and_list_instruction(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        ex_id = await self._create_exercise(auth_client, tag)

        resp = await auth_client.post(
            f"{self.prefix}/{ex_id}/instructions/",
            json={"description": "Deite no banco", "step_order": 1},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["description"] == "Deite no banco"
        assert data["step_order"] == 1

        list_resp = await auth_client.get(f"{self.prefix}/{ex_id}/instructions/")
        assert list_resp.status_code == 200
        assert len(list_resp.json()) >= 1

    async def test_create_second_instruction(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        ex_id = await self._create_exercise(auth_client, tag)

        await auth_client.post(
            f"{self.prefix}/{ex_id}/instructions/",
            json={"description": "Step 1", "step_order": 1},
        )
        resp = await auth_client.post(
            f"{self.prefix}/{ex_id}/instructions/",
            json={"description": "Step 2", "step_order": 2},
        )
        assert resp.status_code == 201

    async def test_create_instruction_exercise_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000/instructions/",
            json={"description": "Step 1"},
        )
        assert resp.status_code == 404

    async def test_list_instructions_exercise_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.get(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000/instructions/",
        )
        assert resp.status_code == 404

    async def test_update_instruction(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        ex_id = await self._create_exercise(auth_client, tag)

        created = (await auth_client.post(
            f"{self.prefix}/{ex_id}/instructions/",
            json={"description": "Old description", "step_order": 1},
        )).json()

        resp = await auth_client.patch(
            f"{self.prefix}/{ex_id}/instructions/{created['id']}",
            json={"description": "New description"},
        )
        assert resp.status_code == 200
        assert resp.json()["description"] == "New description"

    async def test_update_instruction_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.patch(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000/instructions/00000000-0000-0000-0000-000000000000",
            json={"description": "No matter"},
        )
        assert resp.status_code == 404

    async def test_delete_instruction(self, auth_client: AsyncClient):
        from uuid import uuid4
        tag = uuid4().hex[:8]
        ex_id = await self._create_exercise(auth_client, tag)

        created = (await auth_client.post(
            f"{self.prefix}/{ex_id}/instructions/",
            json={"description": "Delete me", "step_order": 1},
        )).json()

        resp = await auth_client.delete(
            f"{self.prefix}/{ex_id}/instructions/{created['id']}",
        )
        assert resp.status_code == 204

    async def test_delete_instruction_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.delete(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000/instructions/00000000-0000-0000-0000-000000000000",
        )
        assert resp.status_code == 404
