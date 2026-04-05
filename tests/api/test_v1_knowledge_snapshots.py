"""Интеграционные тесты /api/v1/knowledge-snapshots (сценарий B)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from tests.conftest import TELEGRAM_HEADERS


async def test_create_knowledge_snapshot(client: AsyncClient) -> None:
    r = await client.post(
        "/api/v1/knowledge-snapshots",
        json={
            "topic": "дроби",
            "level": "proficient",
            "comment": "ДЗ сделано",
            "source": "homework",
        },
        headers=TELEGRAM_HEADERS,
    )
    assert r.status_code == 201
    data = r.json()
    assert data["topic"] == "дроби"
    assert data["level"] == "proficient"
    assert data["channel"] == "telegram"
    assert data["external_user_id"] == "4242"
    assert data["source"] == "homework"
    assert "id" in data
    assert "recorded_at" in data


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({"topic": "тема"}, id="missing_level"),
        pytest.param({"topic": "", "level": "developing"}, id="empty_topic"),
    ],
)
async def test_create_knowledge_snapshot_validation_errors(
    client: AsyncClient,
    payload: dict,
) -> None:
    """Невалидное тело запроса — 422."""
    response = await client.post(
        "/api/v1/knowledge-snapshots",
        json=payload,
        headers=TELEGRAM_HEADERS,
    )
    assert response.status_code == 422
