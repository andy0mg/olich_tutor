"""HTTP-клиент к backend API v1 (заголовки X-Channel, X-External-User-Id)."""

from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

API_V1 = "/api/v1"


class ConversationNotFoundError(Exception):
    """Диалог не найден (например после рестарта in-memory backend)."""


class BackendApiClient:
    """Тонкая обёртка над httpx; не импортирует пакет backend."""

    def __init__(
        self,
        http: httpx.AsyncClient,
        base_url: str,
        *,
        channel: str = "telegram",
    ) -> None:
        self._http = http
        self._base = base_url.rstrip("/")
        self._channel = channel

    def _headers(self, external_user_id: str) -> dict[str, str]:
        return {
            "X-Channel": self._channel,
            "X-External-User-Id": external_user_id,
            "Content-Type": "application/json",
        }

    async def create_conversation(
        self,
        external_user_id: str,
        *,
        topic: str | None = None,
    ) -> str:
        body: dict[str, Any] = {}
        if topic is not None:
            body["topic"] = topic
        url = f"{self._base}{API_V1}/conversations"
        r = await self._http.post(url, headers=self._headers(external_user_id), json=body)
        self._log_error_if_needed(r, "create_conversation", url)
        r.raise_for_status()
        data = r.json()
        return str(data["id"])

    async def post_message(
        self,
        conversation_id: str,
        external_user_id: str,
        content: str,
        *,
        image_base64: str | None = None,
        image_mime_type: str | None = None,
    ) -> str:
        body: dict[str, Any] = {"content": content}
        if image_base64 is not None and image_mime_type is not None:
            body["image_base64"] = image_base64
            body["image_mime_type"] = image_mime_type
        url = f"{self._base}{API_V1}/conversations/{conversation_id}/messages"
        r = await self._http.post(
            url,
            headers=self._headers(external_user_id),
            json=body,
        )
        if r.status_code == 404:
            raise ConversationNotFoundError()
        self._log_error_if_needed(r, "post_message", url)
        r.raise_for_status()
        data = r.json()
        return str(data["assistant_message"]["content"])

    def _log_error_if_needed(self, response: httpx.Response, op: str, url: str) -> None:
        if response.is_success:
            return
        try:
            body = response.text[:500]
        except Exception:
            body = ""
        logger.warning("%s %s failed: %s %s", op, url, response.status_code, body)
