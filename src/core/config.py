from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "GymTracker API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres_password@db:5432/gymtracker"
    DB_ECHO: bool = False
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
