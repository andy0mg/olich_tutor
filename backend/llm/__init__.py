"""Stateless-клиент к OpenRouter; вызывается из сервисов с готовым списком сообщений."""

from backend.llm.client import LLMClient
from backend.llm.deps import get_llm_client

__all__ = ["LLMClient", "get_llm_client"]
