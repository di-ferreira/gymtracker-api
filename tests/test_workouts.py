import pytest
import pytest_asyncio
import bcrypt
from uuid import uuid4
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator


class TestWorkouts:
    prefix = "/api/v1/workouts"
    admin_prefix = "/api/v1/admin/catalog"

    @pytest_asyncio.fixture
    async def user_client(
        self, client: AsyncClient, db_session: AsyncSession
    ) -> AsyncGenerator[AsyncClient, None]:
        from src.models.user import User

        tag = uuid4().hex[:8]
        result = await db_session.execute(
            select(User).filter(User.email == f"workout-user-{tag}@test.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email=f"workout-user-{tag}@test.com",
                hashed_password=bcrypt.hashpw(b"workoutpass", bcrypt.gensalt()).decode(),
                name="Workout User",
                role="user",
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": user.email,
            "password": "workoutpass",
        })
        token = login_resp.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
        yield client

    async def _create_prerequisites(
        self, auth_client: AsyncClient, tag: str
    ) -> tuple:
        mg = (await auth_client.post(f"{self.admin_prefix}/muscle-groups/", json={
            "name": f"MG-{tag}", "slug": f"mg-{tag}",
        })).json()
        mvg = (await auth_client.post(f"{self.admin_prefix}/movement-groups/", json={
            "name": f"MVG-{tag}", "slug": f"mvg-{tag}",
        })).json()
        return mg["id"], mvg["id"]

    async def _create_exercise(
        self, auth_client: AsyncClient, tag: str
    ) -> dict:
        muscle_id, movement_id = await self._create_prerequisites(auth_client, tag)
        resp = await auth_client.post(f"{self.admin_prefix}/exercises/", json={
            "name": f"EX-{tag}",
            "movement_group_id": movement_id,
            "muscle_group_id": muscle_id,
        })
        return resp.json()

    async def test_create_workout(self, user_client: AsyncClient):
        resp = await user_client.post(f"{self.prefix}/", json={
            "name": "Treino de Peito",
            "notes": "Meu treino favorito",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Treino de Peito"
        assert data["notes"] == "Meu treino favorito"
        assert "id" in data
        assert "exercises" in data
        assert data["exercises"] == []

    async def test_create_workout_minimal(self, user_client: AsyncClient):
        resp = await user_client.post(f"{self.prefix}/", json={
            "name": "Treino Rápido",
        })
        assert resp.status_code == 201
        assert resp.json()["name"] == "Treino Rápido"

    async def test_list_workouts(self, user_client: AsyncClient):
        await user_client.post(f"{self.prefix}/", json={"name": "W1"})
        await user_client.post(f"{self.prefix}/", json={"name": "W2"})
        resp = await user_client.get(f"{self.prefix}/")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 2

    async def test_list_workouts_other_user_not_visible(
        self, user_client: AsyncClient, db_session: AsyncSession
    ):
        from httpx import ASGITransport
        from src.main import app
        from src.models.user import User

        tag = uuid4().hex[:8]
        other_user = User(
            email=f"other-{tag}@test.com",
            hashed_password=bcrypt.hashpw(b"otherpass", bcrypt.gensalt()).decode(),
            name="Other User",
            role="user",
        )
        db_session.add(other_user)
        await db_session.commit()

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as other_client:
            login_resp = await other_client.post("/api/v1/auth/login", json={
                "email": other_user.email,
                "password": "otherpass",
            })
            token = login_resp.json()["access_token"]
            other_client.headers.update({"Authorization": f"Bearer {token}"})

            await other_client.post(f"{self.prefix}/", json={"name": "Other Workout"})

        resp = await user_client.get(f"{self.prefix}/")
        names = [w["name"] for w in resp.json()]
        assert "Other Workout" not in names

    async def test_get_workout(self, user_client: AsyncClient):
        created = (await user_client.post(f"{self.prefix}/", json={
            "name": "Meu Treino",
        })).json()
        resp = await user_client.get(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Meu Treino"

    async def test_get_workout_not_found(self, user_client: AsyncClient):
        resp = await user_client.get(f"{self.prefix}/00000000-0000-0000-0000-000000000000")
        assert resp.status_code == 404

    async def test_get_workout_other_user_forbidden(
        self, user_client: AsyncClient, db_session: AsyncSession
    ):
        from httpx import ASGITransport
        from src.main import app
        from src.models.user import User

        tag = uuid4().hex[:8]
        other_user = User(
            email=f"other-get-{tag}@test.com",
            hashed_password=bcrypt.hashpw(b"otherpass", bcrypt.gensalt()).decode(),
            name="Other User",
            role="user",
        )
        db_session.add(other_user)
        await db_session.commit()

        created = (await user_client.post(f"{self.prefix}/", json={
            "name": "Private Workout",
        })).json()

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as other_client:
            login_resp = await other_client.post("/api/v1/auth/login", json={
                "email": other_user.email,
                "password": "otherpass",
            })
            other_client.headers.update({
                "Authorization": f"Bearer {login_resp.json()['access_token']}"
            })

            resp = await other_client.get(f"{self.prefix}/{created['id']}")
            assert resp.status_code == 404

    async def test_update_workout(self, user_client: AsyncClient):
        created = (await user_client.post(f"{self.prefix}/", json={
            "name": "Treino Velho",
        })).json()
        resp = await user_client.patch(f"{self.prefix}/{created['id']}", json={
            "name": "Treino Novo",
            "notes": "Atualizado",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Treino Novo"
        assert data["notes"] == "Atualizado"

    async def test_delete_workout(self, user_client: AsyncClient):
        created = (await user_client.post(f"{self.prefix}/", json={
            "name": "Para Deletar",
        })).json()
        resp = await user_client.delete(f"{self.prefix}/{created['id']}")
        assert resp.status_code == 204
        get_resp = await user_client.get(f"{self.prefix}/{created['id']}")
        assert get_resp.status_code == 404

    async def test_add_exercise_to_workout(
        self, user_client: AsyncClient, auth_client: AsyncClient
    ):
        workout = (await user_client.post(f"{self.prefix}/", json={
            "name": "Com Exercícios",
        })).json()
        exercise = await self._create_exercise(auth_client, uuid4().hex[:8])

        resp = await user_client.post(
            f"{self.prefix}/{workout['id']}/exercises/",
            json={
                "exercise_id": exercise["id"],
                "sort_order": 0,
                "sets": 4,
                "reps": 10,
                "weight": 80.0,
                "notes": "Foco na contração",
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["exercise_id"] == exercise["id"]
        assert data["sets"] == 4
        assert data["reps"] == 10
        assert data["weight"] == 80.0
        assert data["notes"] == "Foco na contração"
        assert "exercise" in data
        assert data["exercise"]["id"] == exercise["id"]

    async def test_add_multiple_exercises(
        self, user_client: AsyncClient, auth_client: AsyncClient
    ):
        workout = (await user_client.post(f"{self.prefix}/", json={
            "name": "Full Body",
        })).json()
        ex1 = await self._create_exercise(auth_client, uuid4().hex[:8])
        ex2 = await self._create_exercise(auth_client, uuid4().hex[:8])

        await user_client.post(
            f"{self.prefix}/{workout['id']}/exercises/",
            json={"exercise_id": ex1["id"], "sort_order": 0},
        )
        await user_client.post(
            f"{self.prefix}/{workout['id']}/exercises/",
            json={"exercise_id": ex2["id"], "sort_order": 1},
        )

        resp = await user_client.get(f"{self.prefix}/{workout['id']}")
        assert resp.status_code == 200
        assert len(resp.json()["exercises"]) == 2

    async def test_update_workout_exercise(
        self, user_client: AsyncClient, auth_client: AsyncClient
    ):
        workout = (await user_client.post(f"{self.prefix}/", json={
            "name": "Update EX",
        })).json()
        exercise = await self._create_exercise(auth_client, uuid4().hex[:8])

        created = (await user_client.post(
            f"{self.prefix}/{workout['id']}/exercises/",
            json={"exercise_id": exercise["id"], "sort_order": 0, "sets": 3},
        )).json()

        resp = await user_client.patch(
            f"{self.prefix}/{workout['id']}/exercises/{created['id']}",
            json={"sets": 5, "reps": 12, "weight": 100.0},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["sets"] == 5
        assert data["reps"] == 12
        assert data["weight"] == 100.0

    async def test_remove_exercise_from_workout(
        self, user_client: AsyncClient, auth_client: AsyncClient
    ):
        workout = (await user_client.post(f"{self.prefix}/", json={
            "name": "Remove EX",
        })).json()
        exercise = await self._create_exercise(auth_client, uuid4().hex[:8])

        created = (await user_client.post(
            f"{self.prefix}/{workout['id']}/exercises/",
            json={"exercise_id": exercise["id"], "sort_order": 0},
        )).json()

        resp = await user_client.delete(
            f"{self.prefix}/{workout['id']}/exercises/{created['id']}"
        )
        assert resp.status_code == 204

        workout_resp = await user_client.get(f"{self.prefix}/{workout['id']}")
        assert len(workout_resp.json()["exercises"]) == 0

    async def test_reorder_exercises(
        self, user_client: AsyncClient, auth_client: AsyncClient
    ):
        workout = (await user_client.post(f"{self.prefix}/", json={
            "name": "Reorder",
        })).json()
        ex1 = await self._create_exercise(auth_client, uuid4().hex[:8])
        ex2 = await self._create_exercise(auth_client, uuid4().hex[:8])

        we1 = (await user_client.post(
            f"{self.prefix}/{workout['id']}/exercises/",
            json={"exercise_id": ex1["id"], "sort_order": 0},
        )).json()
        we2 = (await user_client.post(
            f"{self.prefix}/{workout['id']}/exercises/",
            json={"exercise_id": ex2["id"], "sort_order": 1},
        )).json()

        resp = await user_client.put(
            f"{self.prefix}/{workout['id']}/exercises/reorder",
            json={"exercise_ids": [we2["id"], we1["id"]]},
        )
        assert resp.status_code == 200

    async def test_workout_requires_auth(self, client: AsyncClient):
        resp = await client.post(f"{self.prefix}/", json={"name": "No Auth"})
        assert resp.status_code == 401

    async def test_add_exercise_not_found(self, user_client: AsyncClient):
        resp = await user_client.post(
            f"{self.prefix}/00000000-0000-0000-0000-000000000000/exercises/",
            json={"exercise_id": "00000000-0000-0000-0000-000000000000", "sort_order": 0},
        )
        assert resp.status_code == 404

    async def test_workout_exercise_not_found(self, user_client: AsyncClient):
        workout = (await user_client.post(f"{self.prefix}/", json={
            "name": "Not Found",
        })).json()
        resp = await user_client.patch(
            f"{self.prefix}/{workout['id']}/exercises/00000000-0000-0000-0000-000000000000",
            json={"sets": 5},
        )
        assert resp.status_code == 404
