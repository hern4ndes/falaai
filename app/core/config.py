from functools import lru_cache
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "FALA.AI API"
    api_v1_prefix: str = "/api/v1"

    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "fala_ai"
    database_user: str = "falaai"
    database_password: str = "falaaidevpass"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @computed_field
    @property
    def async_database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.database_user}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/"
            f"{self.database_name}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()