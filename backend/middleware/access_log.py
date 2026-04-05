"""Access-лог и заголовок X-Request-ID без тел запросов и секретов."""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("backend.access")

REQUEST_ID_HEADER = "X-Request-ID"


class AccessLogMiddleware(BaseHTTPMiddleware):
    """Генерирует или пробрасывает request id; одна строка лога на ответ."""

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        raw = request.headers.get(REQUEST_ID_HEADER)
        if raw and raw.strip():
            request_id = raw.strip()
        else:
            request_id = str(uuid.uuid4())

        channel = request.headers.get("X-Channel") or "-"
        ext_user = request.headers.get("X-External-User-Id")
        if ext_user is not None:
            ext_user = ext_user.strip() or "-"
        else:
            ext_user = "-"

        started = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - started) * 1000.0

        response.headers[REQUEST_ID_HEADER] = request_id

        path = request.url.path
        logger.info(
            "request_id=%s method=%s path=%s status=%s duration_ms=%.2f channel=%s external_user_id=%s",
            request_id,
            request.method,
            path,
            response.status_code,
            duration_ms,
            channel,
            ext_user,
        )
        return response
