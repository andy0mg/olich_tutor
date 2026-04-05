"""In-memory хранилище для API v1 (MVP в памяти)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi.responses import JSONResponse

from backend.schemas.api_v1 import (
    Channel,
    Conversation,
    ConversationWithMessages,
    CreateConversationRequest,
    CreateKnowledgeSnapshotRequest,
    KnowledgeSnapshot,
    Message,
    MessageTurnResponse,
    PostMessageRequest,
)


def _utcnow() -> datetime:
    return datetime.now(UTC)


@dataclass
class _ConversationData:
    conversation: Conversation
    messages: list[Message] = field(default_factory=list)


class InMemoryApiStore:
    """Хранилище диалогов и снимков знаний в памяти процесса."""

    def __init__(self) -> None:
        self._conversations: dict[UUID, _ConversationData] = {}
        self._snapshots: dict[UUID, KnowledgeSnapshot] = {}

    def create_conversation(
        self,
        channel: Channel,
        external_user_id: str,
        body: CreateConversationRequest,
    ) -> Conversation:
        cid = uuid4()
        now = _utcnow()
        conv = Conversation(
            id=cid,
            channel=channel,
            external_user_id=external_user_id,
            topic=body.topic,
            created_at=now,
            updated_at=now,
        )
        self._conversations[cid] = _ConversationData(conversation=conv)
        return conv

    def get_conversation(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        limit: int,
        cursor: str | None,
    ) -> ConversationWithMessages | JSONResponse:
        data = self._conversations.get(conversation_id)
        if data is None:
            return _not_found_conversation(conversation_id)
        conv = data.conversation
        if conv.channel != channel or conv.external_user_id != external_user_id:
            return _bad_request_mismatch()

        msgs = data.messages
        start = 0
        if cursor:
            try:
                start = int(cursor)
            except ValueError:
                start = 0
        chunk = msgs[start : start + limit]
        next_start = start + len(chunk)
        next_cursor: str | None = str(next_start) if next_start < len(msgs) else None

        return ConversationWithMessages(
            conversation=conv,
            messages=chunk,
            next_cursor=next_cursor,
        )

    def get_messages(self, conversation_id: UUID) -> list[Message] | None:
        """Сообщения диалога или None, если диалога нет."""
        data = self._conversations.get(conversation_id)
        if data is None:
            return None
        return list(data.messages)

    def append_user_message(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        body: PostMessageRequest,
    ) -> Message | JSONResponse:
        data = self._conversations.get(conversation_id)
        if data is None:
            return _not_found_conversation(conversation_id)
        conv = data.conversation
        if conv.channel != channel or conv.external_user_id != external_user_id:
            return _bad_request_mismatch()

        now = _utcnow()
        seq = len(data.messages)
        user_msg = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role="user",
            content=body.content,
            sequence=seq,
            created_at=now,
        )
        data.messages.append(user_msg)
        return user_msg

    def append_assistant_reply(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        assistant_content: str,
    ) -> MessageTurnResponse | JSONResponse:
        data = self._conversations.get(conversation_id)
        if data is None:
            return _not_found_conversation(conversation_id)
        conv = data.conversation
        if conv.channel != channel or conv.external_user_id != external_user_id:
            return _bad_request_mismatch()
        if not data.messages or data.messages[-1].role != "user":
            return _internal_error_inconsistent()

        now = _utcnow()
        seq = len(data.messages)
        user_msg = data.messages[-1]
        assistant_msg = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_content,
            sequence=seq,
            created_at=now,
        )
        data.messages.append(assistant_msg)
        updated = conv.model_copy(update={"updated_at": now})
        data.conversation = updated

        return MessageTurnResponse(
            user_message=user_msg,
            assistant_message=assistant_msg,
            conversation=updated,
        )

    def create_knowledge_snapshot(
        self,
        channel: Channel,
        external_user_id: str,
        body: CreateKnowledgeSnapshotRequest,
    ) -> KnowledgeSnapshot:
        sid = uuid4()
        snap = KnowledgeSnapshot(
            id=sid,
            channel=channel,
            external_user_id=external_user_id,
            topic=body.topic,
            level=body.level,
            comment=body.comment,
            enrollment_id=body.enrollment_id,
            learning_stream_id=body.learning_stream_id,
            source=body.source,
            recorded_at=_utcnow(),
        )
        self._snapshots[sid] = snap
        return snap


def _not_found_conversation(conversation_id: UUID) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "message": "Conversation not found",
            "details": {"resource": "conversation", "id": str(conversation_id)},
        },
    )


def _bad_request_mismatch() -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error": "bad_request",
            "message": "Conversation does not belong to this user",
            "details": None,
        },
    )


def _internal_error_inconsistent() -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
            "details": None,
        },
    )


_store: InMemoryApiStore | None = None


def get_memory_store() -> InMemoryApiStore:
    """Singleton для процесса API; в тестах переопределяется через dependency_overrides."""
    global _store
    if _store is None:
        _store = InMemoryApiStore()
    return _store
