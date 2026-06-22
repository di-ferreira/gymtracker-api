import pytest
from httpx import AsyncClient


class TestMediaUpload:
    prefix = "/api/v1/admin/media"

    async def test_upload_image(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            f"{self.prefix}/upload",
            files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
            params={"folder": "exercises"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["url"].startswith("http")
        assert data["url"].endswith(".jpg")
        assert data["path"].startswith("exercises/")

    async def test_upload_gif(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            f"{self.prefix}/upload",
            files={"file": ("test.gif", b"fake-gif-data", "image/gif")},
            params={"folder": "exercises"},
        )
        assert resp.status_code == 200
        assert resp.json()["filename"].endswith(".gif")

    async def test_upload_invalid_extension(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            f"{self.prefix}/upload",
            files={"file": ("test.exe", b"bad", "application/x-msdownload")},
            params={"folder": "exercises"},
        )
        assert resp.status_code == 400

    async def test_upload_invalid_folder(self, auth_client: AsyncClient):
        resp = await auth_client.post(
            f"{self.prefix}/upload",
            files={"file": ("test.jpg", b"data", "image/jpeg")},
            params={"folder": "invalid"},
        )
        assert resp.status_code == 400

    async def test_upload_requires_admin(self, client: AsyncClient):
        resp = await client.post(
            f"{self.prefix}/upload",
            files={"file": ("test.jpg", b"data", "image/jpeg")},
            params={"folder": "exercises"},
        )
        assert resp.status_code == 401

    async def test_delete_image(self, auth_client: AsyncClient):
        upload = await auth_client.post(
            f"{self.prefix}/upload",
            files={"file": ("delete-test.jpg", b"data", "image/jpeg")},
            params={"folder": "exercises"},
        )
        path = upload.json()["path"]
        resp = await auth_client.delete(f"{self.prefix}/{path}")
        assert resp.status_code == 200
        assert resp.json()["deleted"] is True

    async def test_delete_requires_admin(self, client: AsyncClient):
        resp = await client.delete(
            f"{self.prefix}/exercises/nonexistent.jpg"
        )
        assert resp.status_code == 401
