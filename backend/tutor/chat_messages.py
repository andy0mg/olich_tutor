"""Сборка списка сообщений для stateless LLM из истории доменных Message."""

from __future__ import annotations

from backend.schemas.api_v1 import Message


def build_chat_messages(system: str, stored_messages: list[Message]) -> list[dict]:
    """system + реплики user/assistant по порядку sequence (system в хранилище не хранится)."""
    out: list[dict] = [{"role": "system", "content": system}]
    for m in sorted(stored_messages, key=lambda x: x.sequence):
        if m.role == "system":
            continue
        if m.role == "user" and m.metadata:
            img = m.metadata.get("image")
            if isinstance(img, dict):
                mime = img.get("mime")
                b64 = img.get("b64")
                if isinstance(mime, str) and isinstance(b64, str) and mime.startswith("image/"):
                    url = f"data:{mime};base64,{b64}"
                    out.append(
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": m.content},
                                {"type": "image_url", "image_url": {"url": url}},
                            ],
                        }
                    )
                    continue
        out.append({"role": m.role, "content": m.content})
    return out
