# Задача 07: рефакторинг бота под backend API — summary

## Сделано

- Добавлен `bot/backend_client.py` (`BackendApiClient`, `ConversationNotFoundError`); эндпоинты `/api/v1/conversations` и `.../messages`.
- `bot/handlers/messages.py`: убраны `llm` и `tutor`; идентификация через строковый Telegram id; восстановление диалога при 404 после рестарта API.
- `main.py`: `httpx.AsyncClient` + клиент API вместо `LLMClient`.
- `config.py`, `.env.example`: `BACKEND_BASE_URL`; комментарии про OpenRouter только для backend.
- Обновлены `README.md`, `docs/vision.md`.
- В `docs/tasks/tasklist-backend.md` задача 07 отмечена выполненной.

## Сценарий (B)

Фиксация ДЗ через `POST /api/v1/knowledge-snapshots` в боте не реализована (ранее в боте не было сценария); контракт и backend без изменений.

## Проверка

- `make test`, `make lint`
- Ручной прогон: `make run-backend` → `make run`, диалог в Telegram
