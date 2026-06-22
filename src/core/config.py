from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "GymTracker API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./gymtracker.db"
    DB_ECHO: bool = False

    # Auth
    SECRET_KEY: str = "change-me-to-a-secure-random-value"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Storage
    STORAGE_BACKEND: str = "local"
    MEDIA_DIR: str = "media"
    MEDIA_BASE_URL: str = "http://localhost:8001/media"
    MAX_UPLOAD_SIZE_MB: int = 10

    # S3 (usado apenas quando STORAGE_BACKEND=s3)
    S3_BUCKET: str = "gymtracker-media"
    S3_REGION: str = "us-east-1"
    S3_ENDPOINT: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""

    @property
    def database_url(self) -> str:
        if self.ENVIRONMENT == "development":
            return self.DATABASE_URL
        url = self.DATABASE_URL
        if url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    @property
    def is_sqlite(self) -> bool:
        return "sqlite" in self.database_url

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
