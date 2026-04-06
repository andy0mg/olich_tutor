"""web_auth_codes table for JWT-based web authentication

Revision ID: 002_web_auth_codes
Revises: 001_initial
Create Date: 2026-04-06

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "002_web_auth_codes"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "web_auth_codes",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), primary_key=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "student_id",
            sa.BigInteger(),
            sa.ForeignKey("students.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("used", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "purpose IN ('student_login', 'parent_invite')",
            name="ck_web_auth_codes_purpose",
        ),
    )
    op.create_index("ix_web_auth_codes_code", "web_auth_codes", ["code"], unique=True)
    op.create_index("ix_web_auth_codes_user_id", "web_auth_codes", ["user_id"])


def downgrade() -> None:
    op.drop_table("web_auth_codes")
