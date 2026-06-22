from src.storage.base import StorageBackend
from src.core.config import settings


_backend: StorageBackend | None = None


def get_storage_backend() -> StorageBackend:
    global _backend
    if _backend is not None:
        return _backend

    if settings.STORAGE_BACKEND == "s3":
        from src.storage.s3 import S3Storage
        _backend = S3Storage()
    else:
        from src.storage.local import LocalStorage
        _backend = LocalStorage()

    return _backend
