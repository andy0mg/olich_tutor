# Задача 05: ORM-модели, репозитории и интеграция в backend

**Tasklist:** [docs/tasks/tasklist-database.md](../../../../../tasklist-database.md)

## Реализация (кратко)

- **ORM:** `backend/db/base.py`, `backend/db/models/tables.py` — все таблицы из миграции `001_initial`; `Message.extra_metadata` → колонка `metadata`.
- **Alembic:** `backend/alembic/env.py` — `target_metadata = Base.metadata` после импорта `backend.db.models`.
- **Сессия:** `backend/db/session.py` — `init_engine` / `dispose_engine`, `get_async_session` (commit/rollback).
- **FastAPI:** `backend/app.py` — `lifespan` для engine; `create_app(with_db_lifespan=False)` для тестов без dispose при закрытии клиента.
- **Идентичность:** `backend/services/identity.py` — `get_or_create_student` по `X-Channel` + `X-External-User-Id`.
- **Хранилище:** `backend/services/api_store.py` — `ApiStore` (Protocol), `PostgresApiStore`; зависимость `get_api_store` в `backend/api/deps.py`.
- **Удалено:** `backend/services/memory_store.py` (InMemoryApiStore).
- **Тесты:** `tests/conftest.py` — session engine + TRUNCATE перед каждым тестом; `pytest.ini` — общий event loop для async engine. Требуется `make db-up && make db-migrate`.

## Документы

- [docs/data-model.md](../../../../../data-model.md) — секция HTTP API v1
- [README.md](../../../../../README.md), [docs/vision.md](../../../../../vision.md) — запуск и тесты
