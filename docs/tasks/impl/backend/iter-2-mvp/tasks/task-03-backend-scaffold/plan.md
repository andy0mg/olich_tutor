# Задача 03: каркас backend-сервиса — план

**Итерация:** iter-2-mvp  
**Tasklist:** [docs/tasks/tasklist-backend.md](../../../../../../tasks/tasklist-backend.md)

## Цель

Запускаемый каркас `backend/` по [docs/vision.md](../../../../../../vision.md): слои `api/`, `services/`, `tutor/`, `llm/`, конфиг из `.env`, маршруты `/health` и `/ready`, отдельный процесс от бота.

## Решения

| Решение | Детали |
|--------|--------|
| Точка входа | `python -m backend` ([backend/__main__.py](../../../../../../../backend/__main__.py)), Uvicorn с `backend.app:app`. |
| Настройки | [backend/config.py](../../../../../../../backend/config.py): `BACKEND_HOST`, `BACKEND_PORT`, `LOG_LEVEL` (pydantic-settings, `.env`). |
| Служебные пути | `GET /health`, `GET /ready` — вне публичного [openapi.yaml](../../../../../../../backend/openapi.yaml). |
| Доменные эндпоинты | Не реализуются в этой задаче (итерация, задачи 04–05). |

## Проверка

- `make run-backend` или `python -m backend` из корня репозитория.
- `GET http://127.0.0.1:8000/health` и `/ready` → 200.
