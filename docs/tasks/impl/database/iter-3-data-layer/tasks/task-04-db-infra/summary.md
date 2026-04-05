# Задача 04: инфраструктура БД — summary

## Сделано

- **Docker Compose:** сервис `postgres` (`postgres:16-alpine`), volume `olich_tutor_pg_data`, healthcheck, на хосте порт `5433` → `5432` в контейнере (чтобы не занимать стандартный `5432`, если он уже занят).
- **Конфиг:** `database_url` в [backend/config.py](../../../../../../../backend/config.py); `DATABASE_URL` в примерах `.env`.
- **Alembic:** async [env.py](../../../../../../../backend/alembic/env.py), первая ревизия [001_initial_schema.py](../../../../../../../backend/alembic/versions/001_initial_schema.py) по физической модели из [data-model.md](../../../../../../../docs/data-model.md).
- **Makefile:** `db-up`, `db-down`, `db-reset`, `db-migrate`, `db-shell`.
- **Документация:** [README.md](../../../../../../../README.md), [docs/vision.md](../../../../../../../docs/vision.md).

## Заметки

- Интеграция SQLAlchemy в приложение и репозитории — задача 05.
- Проверка миграций на живой PostgreSQL требует запущенного Docker (`make db-up`).
