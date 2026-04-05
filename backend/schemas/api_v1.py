"""Модели тел запросов/ответов для /api/v1 (MVP-заглушки, задача iter-2-04)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

Channel = Literal["telegram", "web"]
KnowledgeLevel = Literal["needs_work", "developing", "proficient", "mastered"]
MessageRole = Literal["user", "assistant", "system"]
SnapshotSource = Literal["homework", "self_report", "tutor"]


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: dict | None = None


class CreateConversationRequest(BaseModel):
    topic: str | None = None


class Conversation(BaseModel):
    id: UUID
    channel: Channel
    external_user_id: str
    topic: str | None = None
    created_at: datetime
    updated_at: datetime


class Message(BaseModel):
    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    sequence: int
    created_at: datetime


class ConversationWithMessages(BaseModel):
    conversation: Conversation
    messages: list[Message]
    next_cursor: str | None = None


class PostMessageRequest(BaseModel):
    content: str = Field(..., min_length=1)


class MessageTurnResponse(BaseModel):
    user_message: Message
    assistant_message: Message
    conversation: Conversation


class CreateKnowledgeSnapshotRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    level: KnowledgeLevel
    comment: str | None = None
    enrollment_id: UUID | None = None
    learning_stream_id: UUID | None = None
    source: SnapshotSource = "homework"


class KnowledgeSnapshot(BaseModel):
    id: UUID
    channel: Channel
    external_user_id: str
    topic: str
    level: KnowledgeLevel
    comment: str | None = None
    enrollment_id: UUID | None = None
    learning_stream_id: UUID | None = None
    source: SnapshotSource
    recorded_at: datetime
