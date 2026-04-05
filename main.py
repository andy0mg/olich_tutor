"""Точка входа: логирование, бот, polling."""

import asyncio
import logging
import sys

import httpx
from aiogram import Bot, Dispatcher

from bot.backend_client import BackendApiClient
from bot.handlers import create_messages_router
from config import Settings


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )


async def main() -> None:
    settings = Settings()
    setup_logging(settings.log_level)

    timeout = httpx.Timeout(120.0, connect=10.0)
    async with httpx.AsyncClient(timeout=timeout) as http:
        api = BackendApiClient(http, settings.backend_base_url)
        bot = Bot(token=settings.telegram_token)
        dp = Dispatcher()
        dp.include_router(create_messages_router(api))

        log = logging.getLogger(__name__)
        log.info("Starting polling (backend=%s)...", settings.backend_base_url)
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
