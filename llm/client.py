"""OpenAI-compatible client for OpenRouter."""

import logging

from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class LLMClient:
    """Обёртка над OpenAI SDK: stateless, готовый `messages[]` на входе."""

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._model = model
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def chat(self, messages: list[dict]) -> str:
        """Отправить диалог в модель и вернуть текст ответа ассистента."""
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
            )
        except Exception:
            logger.exception("LLM request failed")
            raise

        choice = response.choices[0]
        content = choice.message.content
        if content is None:
            return ""
        return content
