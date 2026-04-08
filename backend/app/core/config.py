from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_env: str = "development"
    app_name: str = "Academic Writing Copilot API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = True

    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60 * 24

    database_url: str = "sqlite:///./academic_copilot.db"
    redis_url: str = "redis://localhost:6379/0"
    celery_task_always_eager: bool = True

    crossref_base_url: str = "https://api.crossref.org"
    crossref_mailto: str = "yourmail@example.com"

    semantic_scholar_base_url: str = "https://api.semanticscholar.org/graph/v1"
    semantic_scholar_api_key: str | None = None

    llm_provider: str = "heuristic"
    llm_api_key: str | None = None

    cors_origins: List[str] = ["http://localhost:3000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
