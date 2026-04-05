# Задача 02: контракты API — план

**Итерация:** iter-2-mvp  
**Tasklist:** [docs/tasks/tasklist-backend.md](../../../../../../tasks/tasklist-backend.md)

## Цель

Зафиксировать публичный HTTP API до реализации эндпоинтов: сценарии (A) вопрос репетитору и (B) фиксация выполненного ДЗ; OpenAPI; единый формат ошибок; версия `/api/v1`.

## Решения

| Решение | Детали |
|--------|--------|
| Идентификация клиента | Обязательные заголовки `X-Channel` и `X-External-User-Id` на всех операциях (без дублирования в теле). |
| Версия API | Префикс пути `/api/v1`; `info.version` в OpenAPI — версия документа спецификации. |
| Ошибки | Схема `ErrorResponse`: `error`, `message`, опционально `details` (object, nullable). Статусы: 400, 404, 422; тело 422 совместимо с типичным ответом FastAPI (`detail`). |
| Артефакт | [backend/openapi.yaml](../../../../../../../backend/openapi.yaml) |

## Сценарии в спецификации

- **(A)** `POST /api/v1/conversations`, `POST /api/v1/conversations/{conversation_id}/messages`, `GET /api/v1/conversations/{conversation_id}`.
- **(B)** `POST /api/v1/knowledge-snapshots`.

## Проверка спецификации

После `make install` или `uv sync` / установки зависимостей из [requirements.txt](../../../../../../../requirements.txt):

```bash
uv run python -c "import yaml; from openapi_spec_validator import validate_spec; validate_spec(yaml.safe_load(open('backend/openapi.yaml', encoding='utf-8')))"
```

Ожидаемый вывод: без исключений (при необходимости добавить `print('OK')` для наглядности).

Альтернатива: [Redocly CLI](https://redocly.com/docs/cli/) — `npx @redocly/cli lint backend/openapi.yaml`, если доступен Node.js.

## Связанные документы

- [docs/data-model.md](../../../../../../data-model.md) — раздел «Соответствие полей HTTP API v1»
- [docs/adr/adr-002-rest-backend.md](../../../../../../adr/adr-002-rest-backend.md)
