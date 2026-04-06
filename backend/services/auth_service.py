"""Auth business logic: code generation, login, invite flow."""

from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.db.models.tables import (
    GuardianStudentLink,
    Student,
    User,
    UserChannelIdentity,
    WebAuthCode,
)


def _generate_code() -> str:
    return secrets.token_hex(4).upper()


async def create_web_code_for_student(
    session: AsyncSession, user_id: int, student_id: int
) -> str:
    """Generate a one-time code for student web login."""
    code = _generate_code()
    expires = datetime.now(UTC) + timedelta(minutes=settings.web_code_expire_minutes)
    row = WebAuthCode(
        code=code,
        user_id=user_id,
        student_id=student_id,
        purpose="student_login",
        expires_at=expires,
    )
    session.add(row)
    await session.flush()
    return code


async def create_invite_code_for_parent(
    session: AsyncSession, student_id: int
) -> str:
    """Generate an invite code that a parent can use to link and log in."""
    result = await session.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if student is None:
        msg = "Student not found"
        raise ValueError(msg)

    code = _generate_code()
    expires = datetime.now(UTC) + timedelta(days=7)
    row = WebAuthCode(
        code=code,
        user_id=student.user_id,
        student_id=student_id,
        purpose="parent_invite",
        expires_at=expires,
    )
    session.add(row)
    await session.flush()
    return code


async def exchange_student_code(
    session: AsyncSession, code: str
) -> tuple[User, Student, str] | None:
    """Exchange a student_login code for (user, student, role). Returns None on failure."""
    result = await session.execute(
        select(WebAuthCode).where(
            WebAuthCode.code == code,
            WebAuthCode.purpose == "student_login",
            WebAuthCode.used.is_(False),
        )
    )
    auth_code = result.scalar_one_or_none()
    if auth_code is None or auth_code.expires_at < datetime.now(UTC):
        return None

    auth_code.used = True

    user_result = await session.execute(select(User).where(User.id == auth_code.user_id))
    user = user_result.scalar_one()

    student_result = await session.execute(
        select(Student).where(Student.user_id == user.id)
    )
    student = student_result.scalar_one()

    await _ensure_web_identity(session, user.id, str(user.id))
    await session.flush()
    return user, student, "student"


async def exchange_invite_code(
    session: AsyncSession, code: str, display_name: str
) -> tuple[User, str] | None:
    """Exchange a parent_invite code: create parent user, link to student, return (user, role)."""
    result = await session.execute(
        select(WebAuthCode).where(
            WebAuthCode.code == code,
            WebAuthCode.purpose == "parent_invite",
            WebAuthCode.used.is_(False),
        )
    )
    auth_code = result.scalar_one_or_none()
    if auth_code is None or auth_code.expires_at < datetime.now(UTC):
        return None

    auth_code.used = True

    parent_user = User()
    session.add(parent_user)
    await session.flush()

    await _ensure_web_identity(session, parent_user.id, str(parent_user.id))

    link = GuardianStudentLink(
        parent_user_id=parent_user.id,
        student_id=auth_code.student_id,
        status="active",
    )
    session.add(link)
    await session.flush()

    return parent_user, "parent"


async def _ensure_web_identity(session: AsyncSession, user_id: int, external_id: str) -> None:
    """Add a web channel identity if not already present."""
    result = await session.execute(
        select(UserChannelIdentity).where(
            UserChannelIdentity.user_id == user_id,
            UserChannelIdentity.channel == "web",
        )
    )
    if result.scalar_one_or_none() is None:
        session.add(
            UserChannelIdentity(
                user_id=user_id,
                channel="web",
                external_user_id=external_id,
            )
        )


async def get_user_role(session: AsyncSession, user_id: int) -> str:
    """Determine role: 'parent' if has active guardian links, else 'student'."""
    result = await session.execute(
        select(GuardianStudentLink).where(
            GuardianStudentLink.parent_user_id == user_id,
            GuardianStudentLink.status == "active",
        ).limit(1)
    )
    if result.scalar_one_or_none() is not None:
        return "parent"
    return "student"


async def get_student_for_user(session: AsyncSession, user_id: int) -> Student | None:
    result = await session.execute(select(Student).where(Student.user_id == user_id))
    return result.scalar_one_or_none()
