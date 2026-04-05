"""Текстовые сообщения и команда /start."""

import logging

import httpx
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.backend_client import BackendApiClient, ConversationNotFoundError
from bot.telegram_math import plain_math_for_telegram

logger = logging.getLogger(__name__)


def create_messages_router(api: BackendApiClient) -> Router:
    router = Router(name="messages")
    conversation_by_user: dict[int, str] = {}

    @router.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        user = message.from_user
        if not user:
            return
        user_id = user.id
        ext_id = str(user_id)
        try:
            cid = await api.create_conversation(ext_id)
            conversation_by_user[user_id] = cid
        except Exception:
            logger.exception("cmd_start: create_conversation failed for user_id=%s", user_id)
            await message.answer(
                "Не удалось связаться с сервером. Проверь, что backend запущен, и попробуй снова.",
            )
            return
        await message.answer(
            "Привет! Я AI-репетитор по математике. Напиши тему или вопрос — "
            "объясню или помогу с задачей.",
        )

    @router.message()
    async def on_text(message: Message) -> None:
        if not message.text:
            return
        user = message.from_user
        if not user:
            return
        user_id = user.id
        ext_id = str(user_id)

        async def ensure_conversation_id() -> str:
            cid = conversation_by_user.get(user_id)
            if cid is None:
                cid = await api.create_conversation(ext_id)
                conversation_by_user[user_id] = cid
            return cid

        try:
            cid = await ensure_conversation_id()
            try:
                raw_reply = await api.post_message(cid, ext_id, message.text)
            except ConversationNotFoundError:
                cid = await api.create_conversation(ext_id)
                conversation_by_user[user_id] = cid
                raw_reply = await api.post_message(cid, ext_id, message.text)
            reply = plain_math_for_telegram(raw_reply)
        except httpx.HTTPError:
            logger.exception("Reply failed for user_id=%s", user_id)
            await message.answer(
                "Сейчас не удалось получить ответ. Попробуй ещё раз позже.",
            )
            return
        except Exception:
            logger.exception("Reply failed for user_id=%s", user_id)
            await message.answer(
                "Сейчас не удалось получить ответ. Попробуй ещё раз позже.",
            )
            return
        await message.answer(reply)

    return router
