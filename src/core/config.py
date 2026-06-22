from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "GymTracker API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./gymtracker.db"
    DB_ECHO: bool = False

    # Auth
    SECRET_KEY: str = "change-me-to-a-secure-random-value"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

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

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
