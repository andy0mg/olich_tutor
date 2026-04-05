# Задача 01: стек и соглашения — summary

**Статус:** завершена  
**Дата:** 2026-04-05

## Сделано

- В [requirements.txt](../../../../../../../requirements.txt) добавлены `fastapi>=0.115`, `uvicorn[standard]>=0.32`.
- [docs/vision.md](../../../../../../vision.md): таблица Backend/LLM дополнена FastAPI и Uvicorn; кратко зафиксирована роль OpenAPI; в блоке архитектурных решений добавлена ссылка на ADR-002.
- [.cursor/rules/conventions.mdc](../../../../../../../.cursor/rules/conventions.mdc): описаны слои `backend/` (api, services, tutor, llm), отдельная точка входа процесса API, переходная модель с корневыми `llm/`/`tutor/`, ориентир по новым целям Makefile.
- [docs/adr/adr-002-rest-backend.md](../../../../../../adr/adr-002-rest-backend.md) и строка в [docs/adr/README.md](../../../../../../adr/README.md).

## Следующий шаг

Задача 02 в [tasklist-backend.md](../../../../../../tasks/tasklist-backend.md): контракты API (OpenAPI), сценарии (A) и (B).
