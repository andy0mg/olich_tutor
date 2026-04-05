# Задача 01: стек и соглашения — план

**Итерация:** iter-2-mvp (итерация 2 по [docs/plan.md](../../../../../../plan.md))  
**Tasklist:** [docs/tasks/tasklist-backend.md](../../../../../../tasks/tasklist-backend.md)

## Цель

Зафиксировать стек REST-backend (FastAPI, Uvicorn), зависимости в репозитории, согласование с [docs/vision.md](../../../../../../vision.md) и [docs/adr/](../../../../../../adr/README.md), правила в [.cursor/rules/conventions.mdc](../../../../../../../.cursor/rules/conventions.mdc).

## Решения

| Решение | Детали |
|--------|--------|
| API | FastAPI |
| Сервер | `uvicorn[standard]` |
| Зависимости | `requirements.txt` (без перехода на pyproject в рамках задачи) |
| ADR | [ADR-002](../../../../../../adr/adr-002-rest-backend.md) |

## Шаги (выполнение)

1. Добавить `fastapi`, `uvicorn[standard]` в `requirements.txt`.
2. Обновить `docs/vision.md`: таблица Backend/LLM, абзац про OpenAPI, ссылка на ADR-002.
3. Расширить `conventions.mdc`: слои `backend/`, отдельная точка входа API, переход `llm/`/`tutor/` у корня → `backend/`.
4. Добавить `docs/adr/adr-002-rest-backend.md`, строка в `docs/adr/README.md`.

## Проверка

- `make install` проходит.
- DoD из tasklist: стек не противоречит vision; секреты только из `.env`; conventions отражают пути backend.
