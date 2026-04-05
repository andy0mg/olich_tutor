"""Общие фикстуры API-тестов.

Изоляция: каждый тест получает новое приложение и пустой InMemoryApiStore
(dependency_overrides), без общего глобального состояния между тестами.

Политика: интеграционные сценарии через httpx + ASGI; LLM подменяется через
`dependency_overrides` (`get_llm_client`); новые эндпоинты — happy-path и ключевые 4xx.
"""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from backend.app import create_app
from backend.llm.deps import get_llm_client
from backend.services.memory_store import InMemoryApiStore, get_memory_store
from bot.backend_client import BackendApiClient

TELEGRAM_HEADERS = {"X-Channel": "telegram", "X-External-User-Id": "4242"}


class FakeLLMClient:
    """Подмена LLM для тестов API без сети."""

    def __init__(self, reply: str = "mock-assistant-reply") -> None:
        self.reply = reply
        self.last_messages: list[dict] | None = None

    async def chat(self, messages: list[dict]) -> str:
        self.last_messages = messages
        return self.reply


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    """HTTP-клиент к ASGI-приложению с чистым in-memory store."""
    app = create_app()
    store = InMemoryApiStore()
    fake_llm = FakeLLMClient()
    app.dependency_overrides[get_memory_store] = lambda: store
    app.dependency_overrides[get_llm_client] = lambda: fake_llm
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def bot_backend_client(client: AsyncClient) -> BackendApiClient:
    """Тот же ASGI-стек, что у `client`, но через обёртку бота (интеграционная проверка)."""
    return BackendApiClient(client, "http://test")
