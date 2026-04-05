# Задача 06: документирование backend

**Итерация:** iter-2-mvp  
**Статус:** выполнено

## Цель

Один понятный сценарий онбординга: зависимости, переменные окружения, запуск API, доступ к OpenAPI; синхронизация [README.md](../../../../../../../README.md), [.env.example](../../../../../../../.env.example), [docs/vision.md](../../../../../../../docs/vision.md), [docs/data-model.md](../../../../../../../docs/data-model.md), [docs/integrations.md](../../../../../../../docs/integrations.md), [docs/plan.md](../../../../../../../docs/plan.md).

## Шаги

1. Расширить README: только backend, только бот, полный стек; `make run-backend`, URL `/docs`, `/openapi.json`, файл `backend/openapi.yaml`, `/health`, `/ready`.
2. Обновить `.env.example` с комментариями и группировкой (бот / backend / общие).
3. Vision: таблица Make — добавить `make test`; кратко про OpenAPI (файл + автогенерация).
4. Data-model: уточнить MVP ит.2 — хранение в памяти backend (рядом с таблицей API v1).
5. Integrations: OpenRouter из backend при работе через API; ключ не в логах.
6. Plan.md: итерация 2 — прогресс (backend задокументирован); полное завершение ит.2 — после задач 07–08.

## Проверка

`make install` → `.env` из примера → `make run-backend` → `GET /health`, открыть `/docs`.
