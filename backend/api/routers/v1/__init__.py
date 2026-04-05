"""Маршруты /api/v1."""

from fastapi import APIRouter

from backend.api.routers.v1 import conversations, knowledge_snapshots

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(conversations.router)
v1_router.include_router(knowledge_snapshots.router)
