"""Интеграционные тесты /api/v1/conversations (сценарий A)."""

from __future__ import annotations

from uuid import uuid4

from httpx import ASGITransport, AsyncClient

from backend.app import create_app
from backend.llm.deps import get_llm_client
from tests.conftest import TELEGRAM_HEADERS, FakeLLMClient


async def test_create_and_get_conversation(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/conversations",
        json={"topic": "алгебра"},
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["channel"] == "telegram"
    assert data["external_user_id"] == "4242"
    assert data["topic"] == "алгебра"
    cid = data["id"]

    r2 = await client.get(
        f"/api/v1/conversations/{cid}",
        headers=TELEGRAM_HEADERS,
    )
    assert r2.status_code == 200
    body = r2.json()
    assert body["conversation"]["id"] == cid
    assert body["messages"] == []


async def test_post_message_turn(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/conversations",
        json={},
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 201
    cid = r.json()["id"]

    r2 = await client.post(
        f"/api/v1/conversations/{cid}/messages",
        json={"content": "Что такое квадратное уравнение?"},
        headers=TELEGRAM_HEADERS,
    )
    assert r2.status_code == 200
    turn = r2.json()
    assert turn["user_message"]["role"] == "user"
    assert turn["assistant_message"]["role"] == "assistant"
    assert turn["assistant_message"]["content"] == "mock-assistant-reply"
    assert "conversation" in turn
    assert turn["conversation"]["id"] == cid

    r3 = await client.get(
        f"/api/v1/conversations/{cid}",
        headers=TELEGRAM_HEADERS,
    )
    assert r3.status_code == 200
    assert len(r3.json()["messages"]) == 2


async def test_get_conversation_not_found(client: AsyncClient) -> None:
    missing = uuid4()
    r = await client.get(
        f"/api/v1/conversations/{missing}",
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 404
    err = r.json()
    assert err["error"] == "not_found"
    assert "message" in err


async def test_get_conversation_wrong_user(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/conversations",
        json={},
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 201
    cid = r.json()["id"]
    bad_headers = {**TELEGRAM_HEADERS, "X-External-User-Id": "9999"}
    r2 = await client.get(
        f"/api/v1/conversations/{cid}",
        headers=bad_headers,
    )
    assert r2.status_code == 400
    assert r2.json()["error"] == "bad_request"


async def test_invalid_conversation_uuid(client: AsyncClient) -> None:
    r = await client.get(
        "/api/v1/conversations/not-a-uuid",
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 422


async def test_post_message_image_only_stores_metadata(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/conversations",
        json={},
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 201
    cid = r.json()["id"]
    r2 = await client.post(
        f"/api/v1/conversations/{cid}/messages",
        json={
            "content": "",
            "image_base64": "QQ==",
            "image_mime_type": "image/jpeg",
        },
        headers=TELEGRAM_HEADERS,
    )
    assert r2.status_code == 200
    um = r2.json()["user_message"]
    assert um["content"] == "(Задача по фото)"
    assert um["metadata"] is not None
    assert "image" in um["metadata"]


async def test_post_message_image_requires_mime_pair(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/conversations",
        json={},
        headers=TELEGRAM_HEADERS,
    )
    cid = r.json()["id"]
    r2 = await client.post(
        f"/api/v1/conversations/{cid}/messages",
        json={"content": "текст", "image_base64": "QQ=="},
        headers=TELEGRAM_HEADERS,
    )
    assert r2.status_code == 422


async def test_post_message_empty_content(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/conversations",
        json={},
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 201
    cid = r.json()["id"]
    r2 = await client.post(
        f"/api/v1/conversations/{cid}/messages",
        json={"content": ""},
        headers=TELEGRAM_HEADERS,
    )
    assert r2.status_code == 422


async def test_create_conversation_rejects_request_without_headers(
    client: AsyncClient,
) -> None:
    """Без обязательных заголовков — 422 (как у FastAPI для отсутствующих Header)."""
    response = await client.post("/api/v1/conversations", json={})
    assert response.status_code == 422


async def test_create_conversation_rejects_missing_external_user_id_header(
    client: AsyncClient,
) -> None:
    """Только X-Channel без X-External-User-Id — 422."""
    response = await client.post(
        "/api/v1/conversations",
        json={},
        headers={"X-Channel": "telegram"},
    )
    assert response.status_code == 422


async def test_post_message_with_image_sends_multimodal_to_llm() -> None:
    fake_llm = FakeLLMClient()
    app = create_app(with_db_lifespan=False)
    app.dependency_overrides[get_llm_client] = lambda: fake_llm
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post(
            "/api/v1/conversations",
            json={},
            headers=TELEGRAM_HEADERS,
        )
        assert r.status_code == 201
        cid = r.json()["id"]
        r2 = await ac.post(
            f"/api/v1/conversations/{cid}/messages",
            json={
                "content": "Что на картинке?",
                "image_base64": "QQ==",
                "image_mime_type": "image/jpeg",
            },
            headers=TELEGRAM_HEADERS,
        )
    app.dependency_overrides.clear()
    assert r2.status_code == 200
    assert fake_llm.last_messages is not None
    user_msgs = [m for m in fake_llm.last_messages if m.get("role") == "user"]
    content = user_msgs[-1]["content"]
    assert isinstance(content, list)
    part_types = {p.get("type") for p in content}
    assert part_types == {"text", "image_url"}


class _BrokenLLM:
    async def chat(self, messages: list[dict]) -> str:
        raise RuntimeError("simulated LLM failure")


async def test_post_message_llm_error_returns_internal_error() -> None:
    """Сбой вызова LLM — 500 и тело OpenAPI internal_error."""
    app = create_app(with_db_lifespan=False)
    app.dependency_overrides[get_llm_client] = lambda: _BrokenLLM()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post(
            "/api/v1/conversations",
            json={},
            headers=TELEGRAM_HEADERS,
        )
        assert r.status_code == 201
        cid = r.json()["id"]
        r2 = await ac.post(
            f"/api/v1/conversations/{cid}/messages",
            json={"content": "вопрос"},
            headers=TELEGRAM_HEADERS,
        )
    app.dependency_overrides.clear()
    assert r2.status_code == 500
    err = r2.json()
    assert err["error"] == "internal_error"
    assert err["details"] is None
