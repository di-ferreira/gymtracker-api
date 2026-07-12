from uuid import UUID
import pytest
import pytest_asyncio
import bcrypt
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TestUpdateProfile:
    async def test_update_name(self, auth_client: AsyncClient):
        resp = await auth_client.patch("/api/v1/users/me", json={"name": "New Name"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "New Name"

    async def test_change_password(self, auth_client: AsyncClient, db_session: AsyncSession):
        resp = await auth_client.patch("/api/v1/users/me", json={
            "current_password": "testpass123",
            "new_password": "newpass123",
        })
        assert resp.status_code == 200

        login_resp = await auth_client.post("/api/v1/auth/login", json={
            "email": "admin@test.com",
            "password": "newpass123",
        })
        assert login_resp.status_code == 200

        from src.models.user import User
        user = (await db_session.execute(
            select(User).filter(User.email == "admin@test.com")
        )).scalar_one()
        user.hashed_password = bcrypt.hashpw(b"testpass123", bcrypt.gensalt()).decode()
        await db_session.commit()

    async def test_change_password_wrong_current(self, auth_client: AsyncClient):
        resp = await auth_client.patch("/api/v1/users/me", json={
            "current_password": "wrongpass",
            "new_password": "newpass123",
        })
        assert resp.status_code == 400

    async def test_change_password_missing_current(self, auth_client: AsyncClient):
        resp = await auth_client.patch("/api/v1/users/me", json={
            "new_password": "newpass123",
        })
        assert resp.status_code == 400


class TestGetProfile:
    async def test_get_profile(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/users/me")
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "admin@test.com"

    async def test_get_profile_unauthenticated(self, client: AsyncClient):
        resp = await client.get("/api/v1/users/me")
        assert resp.status_code == 401


class TestDeleteOwnAccount:
    async def test_delete_own_account(self, client: AsyncClient, db_session: AsyncSession):
        import bcrypt
        from src.models.user import User

        user = User(
            email="deleteme@test.com",
            hashed_password=bcrypt.hashpw(b"pass123", bcrypt.gensalt()).decode(),
            name="Delete Me",
            role="user",
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "deleteme@test.com",
            "password": "pass123",
        })
        token = login_resp.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})

        resp = await client.delete("/api/v1/users/me")
        assert resp.status_code == 204

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "deleteme@test.com",
            "password": "pass123",
        })
        assert login_resp.status_code == 401


class TestAdminGetUser:
    @pytest_asyncio.fixture
    async def target_user(self, db_session: AsyncSession) -> dict:
        from src.models.user import User

        result = await db_session.execute(
            select(User).filter(User.email == "target-get@test.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="target-get@test.com",
                hashed_password=bcrypt.hashpw(b"pass123", bcrypt.gensalt()).decode(),
                name="Target Get",
                role="user",
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
        return {"id": str(user.id), "email": user.email}

    async def test_admin_get_user_by_id(
        self, auth_client: AsyncClient, target_user: dict
    ):
        resp = await auth_client.get(f"/api/v1/admin/users/{target_user['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "target-get@test.com"
        assert data["name"] == "Target Get"

    async def test_admin_get_user_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.get(
            "/api/v1/admin/users/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404

    async def test_normal_user_cannot_get_user_by_id(
        self, client: AsyncClient, target_user: dict
    ):
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "target-get@test.com",
            "password": "pass123",
        })
        token = login_resp.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})

        resp = await client.get(f"/api/v1/admin/users/{target_user['id']}")
        assert resp.status_code == 403


class TestAdminDeleteUser:
    @pytest_asyncio.fixture
    async def target_user(self, db_session: AsyncSession) -> dict:
        from src.models.user import User

        result = await db_session.execute(
            select(User).filter(User.email == "target-del@test.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="target-del@test.com",
                hashed_password=bcrypt.hashpw(b"pass123", bcrypt.gensalt()).decode(),
                name="Target Del",
                role="user",
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
        return {"id": str(user.id), "email": user.email}

    async def test_admin_soft_delete_user(
        self, auth_client: AsyncClient, target_user: dict, db_session: AsyncSession
    ):
        resp = await auth_client.delete(f"/api/v1/admin/users/{target_user['id']}")
        assert resp.status_code == 204

        from src.models.user import User
        user = (await db_session.execute(
            select(User).filter(User.id == UUID(target_user["id"]))
        )).scalar_one()
        assert user.is_active is False

    async def test_admin_hard_delete_user(
        self, auth_client: AsyncClient, target_user: dict, db_session: AsyncSession
    ):
        resp = await auth_client.delete(
            f"/api/v1/admin/users/{target_user['id']}?permanent=true"
        )
        assert resp.status_code == 204

        from src.models.user import User
        user = (await db_session.execute(
            select(User).filter(User.id == UUID(target_user["id"]))
        )).scalar_one_or_none()
        assert user is None

    async def test_admin_delete_not_found(self, auth_client: AsyncClient):
        resp = await auth_client.delete(
            "/api/v1/admin/users/00000000-0000-0000-0000-000000000000"
        )
        assert resp.status_code == 404

    async def test_normal_user_cannot_delete_user(
        self, client: AsyncClient, target_user: dict
    ):
        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "target-del@test.com",
            "password": "pass123",
        })
        token = login_resp.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})

        resp = await client.delete(f"/api/v1/admin/users/{target_user['id']}")
        assert resp.status_code == 403


class TestAdminUpdateUser:
    @pytest_asyncio.fixture
    async def target_user(self, client: AsyncClient, db_session: AsyncSession) -> dict:
        from src.models.user import User

        result = await db_session.execute(
            select(User).filter(User.email == "target@test.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="target@test.com",
                hashed_password=bcrypt.hashpw(b"pass123", bcrypt.gensalt()).decode(),
                name="Target User",
                role="user",
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)
        return {"id": str(user.id), "email": user.email}

    async def test_admin_promote_user(
        self, auth_client: AsyncClient, target_user: dict
    ):
        resp = await auth_client.patch(
            f"/api/v1/admin/users/{target_user['id']}",
            json={"role": "admin"},
        )
        assert resp.status_code == 200
        assert resp.json()["role"] == "admin"

    async def test_admin_deactivate_user(
        self, auth_client: AsyncClient, target_user: dict
    ):
        resp = await auth_client.patch(
            f"/api/v1/admin/users/{target_user['id']}",
            json={"is_active": False},
        )
        assert resp.status_code == 200
        assert resp.json()["is_active"] is False

    async def test_normal_user_cannot_update_user(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        from src.models.user import User

        result = await db_session.execute(
            select(User).filter(User.email == "normal@test.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="normal@test.com",
                hashed_password=bcrypt.hashpw(b"pass123", bcrypt.gensalt()).decode(),
                name="Normal User",
                role="user",
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "normal@test.com",
            "password": "pass123",
        })
        token = login_resp.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})

        resp = await client.patch(
            f"/api/v1/admin/users/{user.id}",
            json={"role": "admin"},
        )
        assert resp.status_code == 403

    async def test_admin_update_not_found(
        self, auth_client: AsyncClient
    ):
        resp = await auth_client.patch(
            f"/api/v1/admin/users/00000000-0000-0000-0000-000000000000",
            json={"role": "admin"},
        )
        assert resp.status_code == 404

    async def test_admin_list_users(self, auth_client: AsyncClient):
        resp = await auth_client.get("/api/v1/admin/users/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    async def test_normal_user_cannot_list_users(
        self, client: AsyncClient, db_session: AsyncSession
    ):
        from src.models.user import User

        result = await db_session.execute(
            select(User).filter(User.email == "normal2@test.com")
        )
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="normal2@test.com",
                hashed_password=bcrypt.hashpw(b"pass123", bcrypt.gensalt()).decode(),
                name="Normal User 2",
                role="user",
            )
            db_session.add(user)
            await db_session.commit()
            await db_session.refresh(user)

        login_resp = await client.post("/api/v1/auth/login", json={
            "email": "normal2@test.com",
            "password": "pass123",
        })
        token = login_resp.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})

        resp = await client.get("/api/v1/admin/users/")
        assert resp.status_code == 403
