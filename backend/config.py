"""Настройки процесса HTTP API (загрузка из окружения и `.env`)."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Переменные backend; секреты не хранить в коде."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    log_level: str = "INFO"

    openrouter_api_key: str = Field(
        default="",
        description="OpenRouter API key (пустая строка допустима при моках LLM в тестах)",
    )
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenAI-compatible API base URL",
    )
    llm_model: str = Field(
        default="openai/gpt-4o-mini",
        description="Model id on OpenRouter",
    )
    database_url: str = Field(
        default="postgresql+asyncpg://olich:olich_dev@127.0.0.1:5433/olich_tutor",
        description="Async SQLAlchemy URL (postgresql+asyncpg://…)",
    )
    jwt_secret: str = Field(
        default="change-me-in-production",
        description="Secret key for JWT signing (HS256)",
    )
    jwt_access_expire_minutes: int = Field(default=60, description="Access token TTL in minutes")
    jwt_refresh_expire_days: int = Field(default=30, description="Refresh token TTL in days")
    web_code_expire_minutes: int = Field(default=15, description="One-time web auth code TTL")


settings = Settings()
