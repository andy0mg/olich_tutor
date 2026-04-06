"""Таблицы БД: имена колонок и ограничения совпадают с миграцией 001_initial."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text

from backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    email: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class UserChannelIdentity(Base):
    __tablename__ = "user_channel_identities"
    __table_args__ = (
        CheckConstraint(
            "channel IN ('telegram', 'web')",
            name="ck_user_channel_identities_channel",
        ),
        UniqueConstraint("channel", "external_user_id", name="uq_user_channel_identities_channel_external"),
        Index("ix_user_channel_identities_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    channel: Mapped[str] = mapped_column(Text, nullable=False)
    external_user_id: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (UniqueConstraint("user_id", name="uq_students_user_id"),)

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    grade_or_age_band: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class LearningStream(Base):
    __tablename__ = "learning_streams"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class GuardianStudentLink(Base):
    __tablename__ = "guardian_student_links"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'active', 'rejected', 'revoked', 'expired')",
            name="ck_guardian_student_links_status",
        ),
        Index("ix_guardian_student_links_parent_user_id", "parent_user_id"),
        Index("ix_guardian_student_links_student_id", "student_id"),
        Index(
            "uq_guardian_student_links_active_pair",
            "parent_user_id",
            "student_id",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
        Index(
            "uq_guardian_student_links_pending_pair",
            "parent_user_id",
            "student_id",
            unique=True,
            postgresql_where=text("status = 'pending'"),
        ),
        Index(
            "uq_guardian_student_links_invite_token_hash",
            "invite_token_hash",
            unique=True,
            postgresql_where=text("invite_token_hash IS NOT NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    parent_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    invite_token_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'completed', 'paused')",
            name="ck_enrollments_status",
        ),
        Index("ix_enrollments_student_id", "student_id"),
        Index("ix_enrollments_learning_stream_id", "learning_stream_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    learning_stream_id: Mapped[UUID] = mapped_column(
        ForeignKey("learning_streams.id", ondelete="RESTRICT"), nullable=False
    )
    status: Mapped[str] = mapped_column(Text, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class Conversation(Base):
    __tablename__ = "conversations"
    __table_args__ = (
        CheckConstraint("channel IN ('telegram', 'web')", name="ck_conversations_channel"),
        Index("ix_conversations_student_id_updated_at", "student_id", text("updated_at DESC")),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    channel: Mapped[str] = mapped_column(Text, nullable=False)
    topic: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'assistant', 'system')", name="ck_messages_role"),
        CheckConstraint("sequence >= 0", name="ck_messages_sequence_non_negative"),
        UniqueConstraint("conversation_id", "sequence", name="uq_messages_conversation_id_sequence"),
        Index("ix_messages_conversation_id", "conversation_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    extra_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class WebAuthCode(Base):
    __tablename__ = "web_auth_codes"
    __table_args__ = (
        CheckConstraint(
            "purpose IN ('student_login', 'parent_invite')",
            name="ck_web_auth_codes_purpose",
        ),
        Index("ix_web_auth_codes_code", "code", unique=True),
        Index("ix_web_auth_codes_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    code: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[int | None] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=True
    )
    purpose: Mapped[str] = mapped_column(Text, nullable=False)
    used: Mapped[bool] = mapped_column(Boolean, server_default=text("false"), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )


class KnowledgeSnapshot(Base):
    __tablename__ = "knowledge_snapshots"
    __table_args__ = (
        CheckConstraint(
            "level IN ('needs_work', 'developing', 'proficient', 'mastered')",
            name="ck_knowledge_snapshots_level",
        ),
        CheckConstraint(
            "source IN ('homework', 'self_report', 'tutor')",
            name="ck_knowledge_snapshots_source",
        ),
        Index(
            "ix_knowledge_snapshots_student_id_recorded_at",
            "student_id",
            text("recorded_at DESC"),
        ),
        Index("ix_knowledge_snapshots_enrollment_id", "enrollment_id"),
        Index("ix_knowledge_snapshots_learning_stream_id", "learning_stream_id"),
    )

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    enrollment_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("enrollments.id", ondelete="SET NULL"), nullable=True
    )
    learning_stream_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("learning_streams.id", ondelete="SET NULL"), nullable=True
    )
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    level: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(Text, server_default=text("'homework'"), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("now()"), nullable=False
    )
