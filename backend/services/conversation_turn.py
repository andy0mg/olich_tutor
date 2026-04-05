"""Оркестрация хода диалога: хранилище + сбор истории + LLM."""

from __future__ import annotations

from uuid import UUID

from fastapi.responses import JSONResponse

from backend.llm.client import LLMClient
from backend.schemas.api_v1 import Channel, MessageTurnResponse, PostMessageRequest
from backend.services.memory_store import InMemoryApiStore
from backend.tutor.chat_messages import build_chat_messages
from backend.tutor.prompts import DEFAULT_SYSTEM_PROMPT


def _llm_internal_error() -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
            "details": None,
        },
    )


async def post_message_turn(
    store: InMemoryApiStore,
    llm: LLMClient,
    channel: Channel,
    external_user_id: str,
    conversation_id: UUID,
    body: PostMessageRequest,
) -> MessageTurnResponse | JSONResponse:
    appended = store.append_user_message(conversation_id, channel, external_user_id, body)
    if isinstance(appended, JSONResponse):
        return appended

    messages = store.get_messages(conversation_id)
    if messages is None:
        return _llm_internal_error()

    chat_payload = build_chat_messages(DEFAULT_SYSTEM_PROMPT, messages)
    try:
        assistant_text = await llm.chat(chat_payload)
    except Exception:
        return _llm_internal_error()

    turn = store.append_assistant_reply(conversation_id, channel, external_user_id, assistant_text)
    if isinstance(turn, JSONResponse):
        return turn
    return turn
