# Задача 02: проектирование схемы данных — summary

**Итерация:** iter-3-data-layer  
**Tasklist:** [docs/tasks/tasklist-database.md](../../../../../tasklist-database.md)  
**План:** [plan.md](./plan.md)

## Что сделано

- Создан [plan.md](./plan.md) с решениями по PK (`BIGINT` vs `UUID`), `user_channel_identities`, `guardian_student_links` (статусы, частичные уникальные индексы, токен приглашения в той же таблице), ревью по skill `postgresql-table-design`.
- Обновлён [docs/data-model.md](../../../../../../data-model.md): логическая модель (в т.ч. родитель–ребёнок и идентификация по каналу), физические таблицы PostgreSQL, индексы, физическая ER (Mermaid), переносимость PG/SQLite, таблица соответствия API v1 ↔ БД.

## Передача дальше

- Задача 03: выбор ORM и миграций под эту схему.
- Задача 04: Docker, миграции, Make-команды.
