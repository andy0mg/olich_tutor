"""Разрешение заголовков X-Channel / X-External-User-Id в профиль ученика."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models.tables import Student, User, UserChannelIdentity
from backend.schemas.api_v1 import Channel


async def get_or_create_student(
    session: AsyncSession,
    channel: Channel,
    external_user_id: str,
) -> Student:
    """Возвращает Student для пары канал + внешний id, создавая User и связи при необходимости."""
    result = await session.execute(
        select(UserChannelIdentity).where(
            UserChannelIdentity.channel == channel,
            UserChannelIdentity.external_user_id == external_user_id,
        )
    )
    uci = result.scalar_one_or_none()
    if uci is not None:
        r2 = await session.execute(select(Student).where(Student.user_id == uci.user_id))
        return r2.scalar_one()

    user = User()
    session.add(user)
    await session.flush()

    session.add(
        UserChannelIdentity(
            user_id=user.id,
            channel=channel,
            external_user_id=external_user_id,
        )
    )
    student = Student(
        user_id=user.id,
        display_name=f"{channel}:{external_user_id}",
    )
    session.add(student)
    await session.flush()
    return student
