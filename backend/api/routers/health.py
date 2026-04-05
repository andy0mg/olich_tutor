"""Liveness/readiness; не входят в публичный OpenAPI контракт `/api/v1`."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def health_ready() -> dict[str, str]:
    return {"status": "ready"}
