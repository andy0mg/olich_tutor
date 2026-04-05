"""ORM-модели таблиц (соответствуют alembic 001_initial и docs/data-model.md)."""

from backend.db.base import Base
from backend.db.models.tables import (
    Conversation,
    Enrollment,
    GuardianStudentLink,
    KnowledgeSnapshot,
    LearningStream,
    Message,
    Student,
    User,
    UserChannelIdentity,
)

__all__ = [
    "Base",
    "Conversation",
    "Enrollment",
    "GuardianStudentLink",
    "KnowledgeSnapshot",
    "LearningStream",
    "Message",
    "Student",
    "User",
    "UserChannelIdentity",
]
