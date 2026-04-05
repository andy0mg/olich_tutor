"""Сборка списка сообщений для stateless LLM из истории доменных Message."""

from __future__ import annotations

from backend.schemas.api_v1 import Message


def build_chat_messages(system: str, stored_messages: list[Message]) -> list[dict]:
    """system + реплики user/assistant по порядку sequence (system в хранилище не хранится)."""
    out: list[dict] = [{"role": "system", "content": system}]
    for m in sorted(stored_messages, key=lambda x: x.sequence):
        if m.role == "system":
            continue
        out.append({"role": m.role, "content": m.content})
    return out
