# Задача 05 — summary

## Сделано

- Заменён in-memory store на PostgreSQL через SQLAlchemy 2 async и слой `PostgresApiStore` + протокол `ApiStore`.
- Разрешение пользователя: `User` → `UserChannelIdentity` → `Student` при первом обращении с заголовками v1.
- DI: `Depends(get_async_session)` + `Depends(get_api_store)`; при старте приложения — `init_engine`, при остановке — `dispose_engine`.
- Тесты API переведены на реальную БД (очистка таблиц перед тестом); `asyncio_*_loop_scope = session` в `pytest.ini`.
- Обновлены `README.md`, `docs/data-model.md`, `docs/vision.md`.

## Проверка

- `make db-up && make db-migrate && make test` — зелёный при запущенном Docker.
- Ручной сценарий: `make run-backend` — диалоги и снимки переживают перезапуск при неизменном `DATABASE_URL`.
