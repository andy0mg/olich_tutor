"""Application settings from environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Загрузка и валидация конфигурации из `.env` и окружения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    telegram_token: str = Field(description="Telegram Bot API token")
    openrouter_api_key: str = Field(description="OpenRouter API key")
    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenAI-compatible API base URL",
    )
    llm_model: str = Field(
        default="openai/gpt-4o-mini",
        description="Model id on OpenRouter",
    )
    log_level: str = Field(default="INFO", description="Logging level")
