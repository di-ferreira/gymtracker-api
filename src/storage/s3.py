import boto3
from src.storage.base import StorageBackend
from src.core.config import settings


class S3Storage(StorageBackend):
    def __init__(self) -> None:
        self.bucket = settings.S3_BUCKET
        endpoint = settings.S3_ENDPOINT or None
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            region_name=settings.S3_REGION,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
        )

    async def upload(self, path: str, data: bytes, content_type: str) -> str:
        self.client.put_object(
            Bucket=self.bucket,
            Key=path,
            Body=data,
            ContentType=content_type,
        )
        return self.get_url(path)

    async def delete(self, path: str) -> None:
        self.client.delete_object(Bucket=self.bucket, Key=path)

    def get_url(self, path: str) -> str:
        return f"{settings.MEDIA_BASE_URL}/{path}"
