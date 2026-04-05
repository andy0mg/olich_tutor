"""Снимки знаний: /api/v1/knowledge-snapshots — MVP-заглушки (iter-2-04)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backend.api.deps import ClientContext, get_api_store, get_client_context
from backend.schemas.api_v1 import CreateKnowledgeSnapshotRequest, KnowledgeSnapshot
from backend.services.api_store import ApiStore

router = APIRouter(tags=["knowledge_snapshots"])


@router.post("/knowledge-snapshots", status_code=201, response_model=KnowledgeSnapshot)
async def create_knowledge_snapshot(
    body: CreateKnowledgeSnapshotRequest,
    ctx: Annotated[ClientContext, Depends(get_client_context)],
    store: Annotated[ApiStore, Depends(get_api_store)],
) -> KnowledgeSnapshot | JSONResponse:
    result = await store.create_knowledge_snapshot(ctx.channel, ctx.external_user_id, body)
    if isinstance(result, JSONResponse):
        return result
    return result
