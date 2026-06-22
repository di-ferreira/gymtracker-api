import abc


class StorageBackend(abc.ABC):
    @abc.abstractmethod
    async def upload(self, path: str, data: bytes, content_type: str) -> str:
        ...

    @abc.abstractmethod
    async def delete(self, path: str) -> None:
        ...

    @abc.abstractmethod
    def get_url(self, path: str) -> str:
        ...
