"""Access-лог middleware: X-Request-ID и заголовки клиента в ответе."""

from __future__ import annotations

import uuid

from httpx import ASGITransport, AsyncClient

from backend.app import create_app
from tests.conftest import TELEGRAM_HEADERS


async def test_health_returns_request_id() -> None:
    app = create_app(with_db_lifespan=False)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health")
    assert r.status_code == 200
    assert "X-Request-ID" in r.headers
    uuid.UUID(r.headers["X-Request-ID"])


async def test_request_id_echo_from_client() -> None:
    app = create_app(with_db_lifespan=False)
    rid = "custom-req-id-abc"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/health", headers={"X-Request-ID": rid})
    assert r.headers["X-Request-ID"] == rid


async def test_v1_response_includes_request_id(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/conversations",
        json={},
        headers={**TELEGRAM_HEADERS, "X-Request-ID": "v1-test-rid"},
    )
    assert r.status_code == 201
    assert r.headers["X-Request-ID"] == "v1-test-rid"
