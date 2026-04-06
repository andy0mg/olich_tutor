"""Зависимости FastAPI: контекст клиента по заголовкам или JWT (OpenAPI v1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import get_async_session
from backend.schemas.api_v1 import Channel
from backend.services.api_store import ApiStore, PostgresApiStore
from backend.services.jwt_service import decode_access_token


@dataclass(frozen=True)
class ClientContext:
    channel: Channel
    external_user_id: str


@dataclass(frozen=True)
class JwtUser:
    user_id: int
    role: str


async def get_jwt_user(request: Request) -> JwtUser:
    """Extract user from Bearer JWT token. Raises 401 if missing/invalid."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth_header[7:]
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return JwtUser(user_id=int(payload["sub"]), role=payload["role"])


async def get_optional_jwt_user(request: Request) -> JwtUser | None:
    """Extract JWT user if Bearer header present, else return None."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    token = auth_header[7:]
    payload = decode_access_token(token)
    if payload is None:
        return None
    return JwtUser(user_id=int(payload["sub"]), role=payload["role"])


async def get_client_context(
    request: Request,
    x_channel: Annotated[Channel | None, Header(alias="X-Channel")] = None,
    x_external_user_id: Annotated[str | None, Header(alias="X-External-User-Id")] = None,
) -> ClientContext:
    """Resolve client identity: prefer JWT (web), fall back to headers (bot)."""
    jwt_user = await get_optional_jwt_user(request)
    if jwt_user is not None:
        return ClientContext(channel="web", external_user_id=str(jwt_user.user_id))

    if not x_channel or not x_external_user_id:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["header", "X-Channel"],
                    "msg": "X-Channel and X-External-User-Id required when no Bearer token",
                    "type": "value_error",
                },
            ],
        )
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


async def get_api_store(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ApiStore:
    return PostgresApiStore(session)
