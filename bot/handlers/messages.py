"""Текстовые сообщения и команда /start."""

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.telegram_math import plain_math_for_telegram
from llm.client import LLMClient
from tutor.session import get_or_create_session, start_session

logger = logging.getLogger(__name__)


def create_messages_router(llm: LLMClient) -> Router:
    router = Router(name="messages")

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        user = message.from_user
        user_id = user.id if user else 0
        start_session(user_id)
        await message.answer(
            "Привет! Я AI-репетитор по математике. Напиши тему или вопрос — "
            "объясню или помогу с задачей.",
        )

    @router.message()
    async def on_text(message: Message) -> None:
        if not message.text:
            return
        user = message.from_user
        user_id = user.id if user else 0
        session = get_or_create_session(user_id)
        session.history.append({"role": "user", "content": message.text})
        try:
            raw_reply = await llm.chat(session.history)
            reply = plain_math_for_telegram(raw_reply)
        except Exception:
            logger.exception("Reply failed for user_id=%s", user_id)
            session.history.pop()
            await message.answer(
                "Сейчас не удалось получить ответ. Попробуй ещё раз позже.",
            )
            return
        session.history.append({"role": "assistant", "content": reply})
        await message.answer(reply)

    return router
