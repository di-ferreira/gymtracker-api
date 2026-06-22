import os
import aiofiles
from src.storage.base import StorageBackend
from src.core.config import settings


class LocalStorage(StorageBackend):
    def __init__(self) -> None:
        self.media_dir = settings.MEDIA_DIR

    async def upload(self, path: str, data: bytes, content_type: str) -> str:
        full_path = os.path.join(self.media_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        async with aiofiles.open(full_path, "wb") as f:
            await f.write(data)
        return self.get_url(path)

    async def delete(self, path: str) -> None:
        full_path = os.path.join(self.media_dir, path)
        if os.path.isfile(full_path):
            os.remove(full_path)

    def get_url(self, path: str) -> str:
        return f"{settings.MEDIA_BASE_URL}/{path}"
