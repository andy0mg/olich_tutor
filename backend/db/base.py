"""Declarative base для ORM-моделей SQLAlchemy 2."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Единый Base для Alembic target_metadata и моделей."""
