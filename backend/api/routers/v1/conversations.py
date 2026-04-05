"""Диалоги и сообщения: /api/v1/conversations."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from backend.api.deps import ClientContext, get_client_context
from backend.llm.client import LLMClient
from backend.llm.deps import get_llm_client
from backend.schemas.api_v1 import (
    Conversation,
    ConversationWithMessages,
    CreateConversationRequest,
    MessageTurnResponse,
    PostMessageRequest,
)
from backend.services.conversation_turn import post_message_turn
from backend.services.memory_store import InMemoryApiStore, get_memory_store

router = APIRouter(tags=["conversations"])


@router.post("/conversations", status_code=201, response_model=Conversation)
async def create_conversation(
    body: CreateConversationRequest,
    ctx: Annotated[ClientContext, Depends(get_client_context)],
    store: Annotated[InMemoryApiStore, Depends(get_memory_store)],
) -> Conversation:
    return store.create_conversation(ctx.channel, ctx.external_user_id, body)


@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(
    conversation_id: UUID,
    ctx: Annotated[ClientContext, Depends(get_client_context)],
    store: Annotated[InMemoryApiStore, Depends(get_memory_store)],
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    cursor: Annotated[str | None, Query()] = None,
) -> ConversationWithMessages | JSONResponse:
    result = store.get_conversation(
        conversation_id, ctx.channel, ctx.external_user_id, limit, cursor
    )
    if isinstance(result, JSONResponse):
        return result
    return result


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessageTurnResponse,
)
async def post_conversation_message(
    conversation_id: UUID,
    body: PostMessageRequest,
    ctx: Annotated[ClientContext, Depends(get_client_context)],
    store: Annotated[InMemoryApiStore, Depends(get_memory_store)],
    llm: Annotated[LLMClient, Depends(get_llm_client)],
) -> MessageTurnResponse | JSONResponse:
    result = await post_message_turn(
        store,
        llm,
        ctx.channel,
        ctx.external_user_id,
        conversation_id,
        body,
    )
    if isinstance(result, JSONResponse):
        return result
    return result
