"""Точка входа: логирование, бот, polling."""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from bot.handlers import create_messages_router
from config import Settings
from llm.client import LLMClient


def setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )


async def main() -> None:
    settings = Settings()
    setup_logging(settings.log_level)

    llm = LLMClient(
        api_key=settings.openrouter_api_key,
        base_url=settings.openrouter_base_url,
        model=settings.llm_model,
    )
    bot = Bot(token=settings.telegram_token)
    dp = Dispatcher()
    dp.include_router(create_messages_router(llm))

    log = logging.getLogger(__name__)
    log.info("Starting polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
