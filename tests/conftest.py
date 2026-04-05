"""Общие фикстуры API-тестов.

PostgreSQL: перед прогоном — `make db-up && make db-migrate`.
Движок создаётся в session-фикстуре; таблицы очищаются перед каждым тестом.
Приложение для ASGI без lifespan БД, чтобы не вызывать dispose при закрытии клиента.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from backend.app import create_app
from backend.db.session import dispose_engine, get_engine, init_engine
from backend.llm.deps import get_llm_client
from bot.backend_client import BackendApiClient

TELEGRAM_HEADERS = {"X-Channel": "telegram", "X-External-User-Id": "4242"}

_TRUN = text(
    "TRUNCATE messages, knowledge_snapshots, conversations, enrollments, "
    "guardian_student_links, students, user_channel_identities, users, "
    "learning_streams RESTART IDENTITY CASCADE"
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _engine_lifecycle() -> AsyncIterator[None]:
    init_engine()
    yield
    await dispose_engine()


@pytest.fixture(autouse=True)
async def _clean_tables() -> AsyncIterator[None]:
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.execute(_TRUN)
    yield


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
    """HTTP-клиент к ASGI с реальной БД и подменой LLM."""
    app = create_app(with_db_lifespan=False)
    fake_llm = FakeLLMClient()
    app.dependency_overrides[get_llm_client] = lambda: fake_llm
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def bot_backend_client(client: AsyncClient) -> BackendApiClient:
    """Тот же ASGI-стек, что у `client`, но через обёртку бота (интеграционная проверка)."""
    return BackendApiClient(client, "http://test")
