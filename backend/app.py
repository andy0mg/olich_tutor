"""
Точка сборки FastAPI-приложения.

Запуск процесса API: `python -m backend` (из корня репозитория) или
`uvicorn backend.app:app --host … --port …`.
Не путать с `main.py` в корне — там процесс Telegram-бота.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.api.router import api_router
from backend.config import settings
from backend.db.session import dispose_engine, init_engine
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


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_engine()
    yield
    await dispose_engine()


def create_app(*, with_db_lifespan: bool = True) -> FastAPI:
    """with_db_lifespan=False — для тестов: engine создаётся вне приложения (conftest)."""
    configure_logging(settings.log_level)
    common = dict(
        title="olich_tutor backend",
        version="0.1.0",
        description="Ядро системы; публичный контракт — backend/openapi.yaml.",
    )
    if with_db_lifespan:
        application = FastAPI(**common, lifespan=lifespan)
    else:
        application = FastAPI(**common)
    application.add_middleware(AccessLogMiddleware)
    application.include_router(api_router)
    return application


app = create_app()
