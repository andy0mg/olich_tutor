"""Guardian-student links and parent data endpoints: /api/v1/guardian-links/* and /api/v1/students/*."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.deps import JwtUser, get_jwt_user
from backend.db.models.tables import (
    Conversation as ConversationRow,
)
from backend.db.models.tables import (
    GuardianStudentLink,
    Student,
)
from backend.db.models.tables import (
    KnowledgeSnapshot as KnowledgeSnapshotRow,
)
from backend.db.models.tables import (
    Message as MessageRow,
)
from backend.db.session import get_async_session
from backend.schemas.api_v1 import Conversation, KnowledgeSnapshot

router = APIRouter(tags=["guardian_links"])


class ChildResponse(BaseModel):
    student_id: int
    display_name: str
    grade_or_age_band: str | None = None
    link_status: str


class StudentActivityResponse(BaseModel):
    student_id: int
    display_name: str
    total_conversations: int
    total_messages: int
    last_activity: str | None = None
    recent_conversations: list[Conversation]


@router.get("/guardian-links/children", response_model=list[ChildResponse])
async def list_children(
    jwt_user: Annotated[JwtUser, Depends(get_jwt_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[ChildResponse]:
    result = await session.execute(
        select(GuardianStudentLink, Student)
        .join(Student, GuardianStudentLink.student_id == Student.id)
        .where(
            GuardianStudentLink.parent_user_id == jwt_user.user_id,
            GuardianStudentLink.status == "active",
        )
    )
    rows = result.all()
    return [
        ChildResponse(
            student_id=student.id,
            display_name=student.display_name,
            grade_or_age_band=student.grade_or_age_band,
            link_status=link.status,
        )
        for link, student in rows
    ]


async def _verify_parent_access(
    session: AsyncSession, parent_user_id: int, student_id: int
) -> Student:
    result = await session.execute(
        select(GuardianStudentLink).where(
            GuardianStudentLink.parent_user_id == parent_user_id,
            GuardianStudentLink.student_id == student_id,
            GuardianStudentLink.status == "active",
        )
    )
    if result.scalar_one_or_none() is None:
        raise HTTPException(status_code=403, detail="No active link to this student")

    student_result = await session.execute(
        select(Student).where(Student.id == student_id)
    )
    student = student_result.scalar_one_or_none()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.get("/students/{student_id}/activity", response_model=StudentActivityResponse)
async def get_student_activity(
    student_id: int,
    jwt_user: Annotated[JwtUser, Depends(get_jwt_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> StudentActivityResponse:
    student = await _verify_parent_access(session, jwt_user.user_id, student_id)

    conv_count = await session.scalar(
        select(func.count()).select_from(ConversationRow).where(
            ConversationRow.student_id == student_id
        )
    ) or 0

    msg_count = await session.scalar(
        select(func.count())
        .select_from(MessageRow)
        .join(ConversationRow, MessageRow.conversation_id == ConversationRow.id)
        .where(ConversationRow.student_id == student_id)
    ) or 0

    last_conv_result = await session.execute(
        select(ConversationRow)
        .where(ConversationRow.student_id == student_id)
        .order_by(ConversationRow.updated_at.desc())
        .limit(5)
    )
    recent_rows = list(last_conv_result.scalars().all())
    last_activity = recent_rows[0].updated_at.isoformat() if recent_rows else None

    recent_conversations = [
        Conversation(
            id=c.id,
            channel=c.channel,  # type: ignore[arg-type]
            external_user_id=str(student.user_id),
            topic=c.topic,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        for c in recent_rows
    ]

    return StudentActivityResponse(
        student_id=student_id,
        display_name=student.display_name,
        total_conversations=conv_count,
        total_messages=msg_count,
        last_activity=last_activity,
        recent_conversations=recent_conversations,
    )


@router.get("/students/{student_id}/progress", response_model=list[KnowledgeSnapshot])
async def get_student_progress(
    student_id: int,
    jwt_user: Annotated[JwtUser, Depends(get_jwt_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> list[KnowledgeSnapshot]:
    student = await _verify_parent_access(session, jwt_user.user_id, student_id)

    result = await session.execute(
        select(KnowledgeSnapshotRow)
        .where(KnowledgeSnapshotRow.student_id == student_id)
        .order_by(KnowledgeSnapshotRow.recorded_at.desc())
    )
    rows = list(result.scalars().all())

    return [
        KnowledgeSnapshot(
            id=r.id,
            channel="web",
            external_user_id=str(student.user_id),
            topic=r.topic,
            level=r.level,  # type: ignore[arg-type]
            comment=r.comment,
            enrollment_id=r.enrollment_id,
            learning_stream_id=r.learning_stream_id,
            source=r.source,  # type: ignore[arg-type]
            recorded_at=r.recorded_at,
        )
        for r in rows
    ]
