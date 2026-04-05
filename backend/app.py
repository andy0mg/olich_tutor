"""
Точка сборки FastAPI-приложения.

Запуск процесса API: `python -m backend` (из корня репозитория) или
`uvicorn backend.app:app --host … --port …`.
Не путать с `main.py` в корне — там процесс Telegram-бота.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from backend.api.router import api_router
from backend.config import settings
from backend.middleware import AccessLogMiddleware


def configure_logging(level: str) -> None:
    """Формат и уровень — как в docs/vision.md."""
    numeric = getattr(logging, level.upper(), logging.INFO)
    if not isinstance(numeric, int):
        numeric = logging.INFO
    logging.basicConfig(
        level=numeric,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def create_app() -> FastAPI:
    configure_logging(settings.log_level)
    application = FastAPI(
        title="olich_tutor backend",
        version="0.1.0",
        description="Ядро системы; публичный контракт — backend/openapi.yaml.",
    )
    application.add_middleware(AccessLogMiddleware)
    application.include_router(api_router)
    return application


app = create_app()
