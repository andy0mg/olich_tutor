"""initial schema (docs/data-model.md physical model)

Revision ID: 001_initial
Revises:
Create Date: 2026-04-05

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), primary_key=True),
        sa.Column("email", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "user_channel_identities",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("channel", sa.Text(), nullable=False),
        sa.Column("external_user_id", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "channel IN ('telegram', 'web')",
            name="ck_user_channel_identities_channel",
        ),
    )
    op.create_unique_constraint(
        "uq_user_channel_identities_channel_external",
        "user_channel_identities",
        ["channel", "external_user_id"],
    )
    op.create_index(
        "ix_user_channel_identities_user_id",
        "user_channel_identities",
        ["user_id"],
    )

    op.create_table(
        "students",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), primary_key=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=False),
        sa.Column("grade_or_age_band", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint("user_id", name="uq_students_user_id"),
    )

    op.create_table(
        "learning_streams",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "guardian_student_links",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), primary_key=True),
        sa.Column("parent_user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("student_id", sa.BigInteger(), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("invite_token_hash", sa.Text(), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'active', 'rejected', 'revoked', 'expired')",
            name="ck_guardian_student_links_status",
        ),
    )
    op.create_index(
        "ix_guardian_student_links_parent_user_id",
        "guardian_student_links",
        ["parent_user_id"],
    )
    op.create_index(
        "ix_guardian_student_links_student_id",
        "guardian_student_links",
        ["student_id"],
    )
    op.create_index(
        "uq_guardian_student_links_active_pair",
        "guardian_student_links",
        ["parent_user_id", "student_id"],
        unique=True,
        postgresql_where=sa.text("status = 'active'"),
    )
    op.create_index(
        "uq_guardian_student_links_pending_pair",
        "guardian_student_links",
        ["parent_user_id", "student_id"],
        unique=True,
        postgresql_where=sa.text("status = 'pending'"),
    )
    op.create_index(
        "uq_guardian_student_links_invite_token_hash",
        "guardian_student_links",
        ["invite_token_hash"],
        unique=True,
        postgresql_where=sa.text("invite_token_hash IS NOT NULL"),
    )

    op.create_table(
        "enrollments",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("student_id", sa.BigInteger(), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "learning_stream_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("learning_streams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('active', 'completed', 'paused')",
            name="ck_enrollments_status",
        ),
    )
    op.create_index("ix_enrollments_student_id", "enrollments", ["student_id"])
    op.create_index(
        "ix_enrollments_learning_stream_id",
        "enrollments",
        ["learning_stream_id"],
    )

    op.create_table(
        "conversations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("student_id", sa.BigInteger(), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column("channel", sa.Text(), nullable=False),
        sa.Column("topic", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "channel IN ('telegram', 'web')",
            name="ck_conversations_channel",
        ),
    )
    op.execute(
        sa.text(
            "CREATE INDEX ix_conversations_student_id_updated_at "
            "ON conversations (student_id, updated_at DESC)"
        )
    )

    op.create_table(
        "messages",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "conversation_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("conversations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("role", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "role IN ('user', 'assistant', 'system')",
            name="ck_messages_role",
        ),
        sa.CheckConstraint("sequence >= 0", name="ck_messages_sequence_non_negative"),
    )
    op.create_unique_constraint(
        "uq_messages_conversation_id_sequence",
        "messages",
        ["conversation_id", "sequence"],
    )
    op.create_index(
        "ix_messages_conversation_id",
        "messages",
        ["conversation_id"],
    )

    op.create_table(
        "knowledge_snapshots",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("student_id", sa.BigInteger(), sa.ForeignKey("students.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "enrollment_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("enrollments.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "learning_stream_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("learning_streams.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("topic", sa.Text(), nullable=False),
        sa.Column("level", sa.Text(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column(
            "source",
            sa.Text(),
            server_default=sa.text("'homework'"),
            nullable=False,
        ),
        sa.Column(
            "recorded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "level IN ('needs_work', 'developing', 'proficient', 'mastered')",
            name="ck_knowledge_snapshots_level",
        ),
        sa.CheckConstraint(
            "source IN ('homework', 'self_report', 'tutor')",
            name="ck_knowledge_snapshots_source",
        ),
    )
    op.execute(
        sa.text(
            "CREATE INDEX ix_knowledge_snapshots_student_id_recorded_at "
            "ON knowledge_snapshots (student_id, recorded_at DESC)"
        )
    )
    op.create_index(
        "ix_knowledge_snapshots_enrollment_id",
        "knowledge_snapshots",
        ["enrollment_id"],
    )
    op.create_index(
        "ix_knowledge_snapshots_learning_stream_id",
        "knowledge_snapshots",
        ["learning_stream_id"],
    )


def downgrade() -> None:
    op.drop_table("knowledge_snapshots")
    op.drop_table("messages")
    op.execute(sa.text("DROP INDEX IF EXISTS ix_conversations_student_id_updated_at"))
    op.drop_table("conversations")
    op.drop_table("enrollments")
    op.drop_table("guardian_student_links")
    op.drop_table("learning_streams")
    op.drop_table("students")
    op.drop_table("user_channel_identities")
    op.drop_table("users")
