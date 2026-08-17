from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    max_agent_steps: int = Field(default=5, ge=1, le=20)
    tool_timeout_seconds: int = Field(default=10, ge=1, le=120)
    model_name: str = "not-configured"
    prompt_version: str = "v0"
    index_version: str = "v0"


@lru_cache
def get_settings() -> Settings:
    return Settings()

