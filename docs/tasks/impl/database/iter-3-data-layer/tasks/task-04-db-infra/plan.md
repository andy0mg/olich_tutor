# Задача 04: инфраструктура БД — план

**Tasklist:** [docs/tasks/tasklist-database.md](../../../../../../../docs/tasks/tasklist-database.md)

## Цель

Локальный PostgreSQL, `DATABASE_URL`, первая ревизия Alembic по [docs/data-model.md](../../../../../../../docs/data-model.md), команды `make db-*`.

## Принятые решения

| Вопрос | Решение |
|--------|---------|
| Миграции vs ORM в этой задаче | Ручная ревизия `001_initial_schema.py` (`op.create_*`), без ORM-моделей — задача 05 |
| Alembic sync/async | **Async:** `create_async_engine` + `run_sync(do_run_migrations)` в [backend/alembic/env.py](../../../../../../../backend/alembic/env.py), URL `postgresql+asyncpg://…` |
| Загрузка URL | `DATABASE_URL` из корневого `.env` (путь от `backend/alembic/env.py` к корню репозитория) |
| Docker | [docker-compose.yml](../../../../../../../docker-compose.yml): `postgres:16-alpine`, пользователь/БД `olich` / `olich_tutor`, пароль `olich_dev` (только dev) |

## Чеклист

- [x] `requirements.txt`: sqlalchemy[asyncio], asyncpg, alembic, greenlet
- [x] `backend/config.py`: `database_url` / `DATABASE_URL`
- [x] `.env.example`, `backend/.env.example`
- [x] `docker-compose.yml`
- [x] `backend/alembic.ini`, `env.py`, `versions/001_initial_schema.py`
- [x] Makefile: `db-up`, `db-down`, `db-reset`, `db-migrate`, `db-shell`
- [x] `README.md`, `docs/vision.md`

## Проверка

- `make db-up && make db-migrate` — при запущенном Docker.
- `make db-reset` — пересоздание volume и миграций.
- `make db-shell` — `\dt` показывает таблицы схемы.
