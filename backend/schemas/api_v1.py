"""Модели тел запросов/ответов для /api/v1 (MVP-заглушки, задача iter-2-04)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

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
    metadata: dict | None = None


class ConversationWithMessages(BaseModel):
    conversation: Conversation
    messages: list[Message]
    next_cursor: str | None = None


class PostMessageRequest(BaseModel):
    """Текст и/или изображение (base64). Пустой текст допустим, если есть картинка."""

    content: str = Field(default="", max_length=50000)
    image_base64: str | None = Field(default=None, max_length=20_000_000)
    image_mime_type: str | None = Field(default=None, max_length=128)

    @model_validator(mode="after")
    def content_or_image_and_pair(self) -> PostMessageRequest:
        has_b64 = self.image_base64 is not None
        has_mime = self.image_mime_type is not None
        if has_b64 != has_mime:
            msg = "image_base64 и image_mime_type задаются вместе или оба отсутствуют"
            raise ValueError(msg)
        has_image = bool(self.image_base64 and self.image_mime_type)
        if not self.content.strip() and not has_image:
            msg = "Нужен непустой текст или изображение"
            raise ValueError(msg)
        return self


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
