# Задача 03: каркас backend-сервиса — summary

**Статус:** выполнено

## Сделано

- Пакет [backend/](../../../../../../../backend/): [app.py](../../../../../../../backend/app.py) (`create_app`, логирование по vision), [config.py](../../../../../../../backend/config.py), [api/router.py](../../../../../../../backend/api/router.py), [api/routers/health.py](../../../../../../../backend/api/routers/health.py).
- Заготовки [services/](../../../../../../../backend/services/), [tutor/](../../../../../../../backend/tutor/), [llm/](../../../../../../../backend/llm/).
- Запуск: [backend/__main__.py](../../../../../../../backend/__main__.py); цель `make run-backend` в [Makefile](../../../../../../../Makefile).
- [.env.example](../../../../../../../.env.example): `BACKEND_HOST`, `BACKEND_PORT`; [docs/vision.md](../../../../../../vision.md) — пример `.env` и таблица Make-команд.

## Проверка

- `ruff check backend` — без замечаний.
- Локально: Uvicorn на `:8000`, `GET /health` и `GET /ready` возвращают 200.
