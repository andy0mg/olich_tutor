"""Зависимости FastAPI: контекст клиента по заголовкам (OpenAPI v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Header, HTTPException

from backend.schemas.api_v1 import Channel


@dataclass(frozen=True)
class ClientContext:
    channel: Channel
    external_user_id: str


async def get_client_context(
    x_channel: Annotated[Channel, Header(alias="X-Channel")],
    x_external_user_id: Annotated[str, Header(alias="X-External-User-Id")],
) -> ClientContext:
    trimmed = x_external_user_id.strip()
    if not trimmed:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["header", "X-External-User-Id"],
                    "msg": "must not be empty",
                    "type": "value_error",
                },
            ],
        )
    return ClientContext(channel=x_channel, external_user_id=trimmed)
