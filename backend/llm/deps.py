"""Зависимости FastAPI: singleton LLM-клиента."""

from __future__ import annotations

from backend.config import settings
from backend.llm.client import LLMClient

_llm: LLMClient | None = None


def get_llm_client() -> LLMClient:
    """Один экземпляр на процесс; в тестах переопределяется через dependency_overrides."""
    global _llm
    if _llm is None:
        _llm = LLMClient(
            api_key=settings.openrouter_api_key,
            base_url=settings.openrouter_base_url,
            model=settings.llm_model,
        )
    return _llm
