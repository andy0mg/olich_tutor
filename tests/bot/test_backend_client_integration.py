"""Интеграция `bot.backend_client.BackendApiClient` с FastAPI-приложением (ASGI).

Паттерн как в fastapi-templates: `AsyncClient(transport=ASGITransport(app=app))`
и вызовы к реальным маршрутам; LLM и store подменены фикстурой `client`.
"""

from __future__ import annotations

from uuid import uuid4

import pytest
from httpx import AsyncClient

from bot.backend_client import BackendApiClient, ConversationNotFoundError


async def test_bot_client_create_conversation_and_message_turn(
    bot_backend_client: BackendApiClient,
) -> None:
    ext_id = "tg-user-4242"
    cid = await bot_backend_client.create_conversation(ext_id, topic="алгебра")
    assert cid

    reply = await bot_backend_client.post_message(
        cid,
        ext_id,
        "Что такое квадратное уравнение?",
    )
    assert reply == "mock-assistant-reply"


async def test_bot_client_post_message_raises_when_conversation_missing(
    bot_backend_client: BackendApiClient,
) -> None:
    missing = str(uuid4())
    with pytest.raises(ConversationNotFoundError):
        await bot_backend_client.post_message(missing, "4242", "текст")


async def test_bot_client_conversation_id_accepted_by_raw_api_client(
    bot_backend_client: BackendApiClient,
    client: AsyncClient,
) -> None:
    """Диалог, созданный через обёртку бота, читается тем же ASGI-приложением."""
    ext_id = "777"
    cid = await bot_backend_client.create_conversation(ext_id)
    r = await client.get(
        f"/api/v1/conversations/{cid}",
        headers={"X-Channel": "telegram", "X-External-User-Id": ext_id},
    )
    assert r.status_code == 200
    assert r.json()["conversation"]["id"] == cid
