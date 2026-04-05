"""Персистентное хранилище API v1 (PostgreSQL + SQLAlchemy async)."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Protocol, runtime_checkable
from uuid import UUID, uuid4

from fastapi.responses import JSONResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.tables import Conversation as ConversationRow
from backend.db.models.tables import Enrollment
from backend.db.models.tables import KnowledgeSnapshot as KnowledgeSnapshotRow
from backend.db.models.tables import Message as MessageRow
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
from backend.services.identity import get_or_create_student


def _utcnow() -> datetime:
    return datetime.now(UTC)


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


def _bad_request_enrollment() -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error": "bad_request",
            "message": "Enrollment does not belong to this student",
            "details": None,
        },
    )


def _row_to_message(row: MessageRow) -> Message:
    return Message(
        id=row.id,
        conversation_id=row.conversation_id,
        role=row.role,  # type: ignore[arg-type]
        content=row.content,
        sequence=row.sequence,
        created_at=row.created_at,
    )


def _row_to_conversation(row: ConversationRow, external_user_id: str) -> Conversation:
    return Conversation(
        id=row.id,
        channel=row.channel,  # type: ignore[arg-type]
        external_user_id=external_user_id,
        topic=row.topic,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


@runtime_checkable
class ApiStore(Protocol):
    async def create_conversation(
        self,
        channel: Channel,
        external_user_id: str,
        body: CreateConversationRequest,
    ) -> Conversation: ...

    async def get_conversation(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        limit: int,
        cursor: str | None,
    ) -> ConversationWithMessages | JSONResponse: ...

    async def get_messages(self, conversation_id: UUID) -> list[Message] | None: ...

    async def append_user_message(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        body: PostMessageRequest,
    ) -> Message | JSONResponse: ...

    async def append_assistant_reply(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        assistant_content: str,
    ) -> MessageTurnResponse | JSONResponse: ...

    async def create_knowledge_snapshot(
        self,
        channel: Channel,
        external_user_id: str,
        body: CreateKnowledgeSnapshotRequest,
    ) -> KnowledgeSnapshot | JSONResponse: ...


class PostgresApiStore:
    """Реализация ApiStore поверх AsyncSession."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_conversation(
        self,
        channel: Channel,
        external_user_id: str,
        body: CreateConversationRequest,
    ) -> Conversation:
        student = await get_or_create_student(self._session, channel, external_user_id)
        now = _utcnow()
        row = ConversationRow(
            id=uuid4(),
            student_id=student.id,
            channel=channel,
            topic=body.topic,
            created_at=now,
            updated_at=now,
        )
        self._session.add(row)
        await self._session.flush()
        return _row_to_conversation(row, external_user_id)

    async def _load_conversation_for_user(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
    ) -> tuple[ConversationRow, str] | JSONResponse:
        student = await get_or_create_student(self._session, channel, external_user_id)
        result = await self._session.execute(
            select(ConversationRow).where(ConversationRow.id == conversation_id)
        )
        conv = result.scalar_one_or_none()
        if conv is None:
            return _not_found_conversation(conversation_id)
        if conv.student_id != student.id or conv.channel != channel:
            return _bad_request_mismatch()
        return (conv, external_user_id)

    async def get_conversation(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        limit: int,
        cursor: str | None,
    ) -> ConversationWithMessages | JSONResponse:
        loaded = await self._load_conversation_for_user(conversation_id, channel, external_user_id)
        if isinstance(loaded, JSONResponse):
            return loaded
        conv, ext = loaded

        msg_result = await self._session.execute(
            select(MessageRow)
            .where(MessageRow.conversation_id == conversation_id)
            .order_by(MessageRow.sequence)
        )
        rows = list(msg_result.scalars().all())
        msgs = [_row_to_message(m) for m in rows]

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
            conversation=_row_to_conversation(conv, ext),
            messages=chunk,
            next_cursor=next_cursor,
        )

    async def get_messages(self, conversation_id: UUID) -> list[Message] | None:
        result = await self._session.execute(
            select(MessageRow)
            .where(MessageRow.conversation_id == conversation_id)
            .order_by(MessageRow.sequence)
        )
        rows = list(result.scalars().all())
        if not rows:
            conv_exists = await self._session.scalar(
                select(func.count()).select_from(ConversationRow).where(ConversationRow.id == conversation_id)
            )
            if conv_exists == 0:
                return None
        return [_row_to_message(m) for m in rows]

    async def append_user_message(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        body: PostMessageRequest,
    ) -> Message | JSONResponse:
        loaded = await self._load_conversation_for_user(conversation_id, channel, external_user_id)
        if isinstance(loaded, JSONResponse):
            return loaded
        conv, _ext = loaded

        max_seq = await self._session.scalar(
            select(func.coalesce(func.max(MessageRow.sequence), -1)).where(
                MessageRow.conversation_id == conversation_id
            )
        )
        assert max_seq is not None
        next_seq = int(max_seq) + 1
        now = _utcnow()
        msg = MessageRow(
            id=uuid4(),
            conversation_id=conversation_id,
            role="user",
            content=body.content,
            sequence=next_seq,
            created_at=now,
        )
        self._session.add(msg)
        conv.updated_at = now
        await self._session.flush()
        return _row_to_message(msg)

    async def append_assistant_reply(
        self,
        conversation_id: UUID,
        channel: Channel,
        external_user_id: str,
        assistant_content: str,
    ) -> MessageTurnResponse | JSONResponse:
        loaded = await self._load_conversation_for_user(conversation_id, channel, external_user_id)
        if isinstance(loaded, JSONResponse):
            return loaded
        conv, ext = loaded

        result = await self._session.execute(
            select(MessageRow)
            .where(MessageRow.conversation_id == conversation_id)
            .order_by(MessageRow.sequence.desc())
            .limit(1)
        )
        last = result.scalar_one_or_none()
        if last is None or last.role != "user":
            return _internal_error_inconsistent()

        user_msg = _row_to_message(last)

        max_seq = await self._session.scalar(
            select(func.coalesce(func.max(MessageRow.sequence), -1)).where(
                MessageRow.conversation_id == conversation_id
            )
        )
        assert max_seq is not None
        next_seq = int(max_seq) + 1
        now = _utcnow()
        assistant_row = MessageRow(
            id=uuid4(),
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_content,
            sequence=next_seq,
            created_at=now,
        )
        self._session.add(assistant_row)
        conv.updated_at = now
        await self._session.flush()

        assistant_msg = _row_to_message(assistant_row)
        updated_conv = _row_to_conversation(conv, ext)

        return MessageTurnResponse(
            user_message=user_msg,
            assistant_message=assistant_msg,
            conversation=updated_conv,
        )

    async def create_knowledge_snapshot(
        self,
        channel: Channel,
        external_user_id: str,
        body: CreateKnowledgeSnapshotRequest,
    ) -> KnowledgeSnapshot | JSONResponse:
        student = await get_or_create_student(self._session, channel, external_user_id)

        if body.enrollment_id is not None:
            er = await self._session.execute(
                select(Enrollment).where(
                    Enrollment.id == body.enrollment_id,
                    Enrollment.student_id == student.id,
                )
            )
            if er.scalar_one_or_none() is None:
                return _bad_request_enrollment()

        row = KnowledgeSnapshotRow(
            id=uuid4(),
            student_id=student.id,
            enrollment_id=body.enrollment_id,
            learning_stream_id=body.learning_stream_id,
            topic=body.topic,
            level=body.level,
            comment=body.comment,
            source=body.source,
            recorded_at=_utcnow(),
        )
        self._session.add(row)
        await self._session.flush()

        return KnowledgeSnapshot(
            id=row.id,
            channel=channel,
            external_user_id=external_user_id,
            topic=row.topic,
            level=row.level,  # type: ignore[arg-type]
            comment=row.comment,
            enrollment_id=row.enrollment_id,
            learning_stream_id=row.learning_stream_id,
            source=row.source,  # type: ignore[arg-type]
            recorded_at=row.recorded_at,
        )
