# Итерация: слой данных (iter-3-data-layer) — summary

**Tasklist:** [docs/tasks/tasklist-database.md](../../../tasklist-database.md)  
**Сводка области:** [docs/tasks/impl/database/summary.md](../summary.md)  
**План итерации:** [plan.md](./plan.md)

## Статус

| | |
|--|--|
| **Прогресс** | 5 из 5 задач завершены (01–05 ✅) |
| **Состояние итерации** | ✅ Завершена |

## Что сделано

- **Задача 01:** сценарии ученика и родителя, матрица «сценарий → сущности», требования к данным и связи родитель–ребёнок — [tasks/task-01-user-scenarios/summary.md](tasks/task-01-user-scenarios/summary.md).
- **Задача 02:** логическая и физическая модель в [docs/data-model.md](../../../../data-model.md), решения в [tasks/task-02-schema-design/](tasks/task-02-schema-design/), аудит по `postgresql-table-design`.
- **Задача 03:** [ADR-003](../../../../adr/adr-003-orm-migrations.md), [план и справка](tasks/task-03-tooling-adr/plan.md), обновлены [vision](../../../../vision.md) и [реестр ADR](../../../../adr/README.md).
- **Задача 04:** Docker PostgreSQL, миграции, Make-команды — [tasks/task-04-db-infra/summary.md](tasks/task-04-db-infra/summary.md).
- **Задача 05:** ORM, `PostgresApiStore`, интеграция в FastAPI — [tasks/task-05-orm-integration/summary.md](tasks/task-05-orm-integration/summary.md).

## Следующие шаги

Итерация закрыта; дальнейшая персистентность и новые сущности — по roadmap и [tasklist-backend.md](../../../tasklist-backend.md).

## Ключевые артефакты

| Артефакт | Где |
|----------|-----|
| Модель данных (логика + физика + ER) | [docs/data-model.md](../../../../data-model.md) |
| ADR по ORM и миграциям | [docs/adr/adr-003-orm-migrations.md](../../../../adr/adr-003-orm-migrations.md) |
| ORM, сессия, хранилище API | `backend/db/`, `backend/services/api_store.py`, `backend/services/identity.py` |
| Миграции | `backend/alembic/versions/` |
| Планы и summary по задачам | [tasks/](tasks/) |

## Обновление документа

Дата последней актуализации: 2026-04-05. План и сводка области — [impl/database/plan.md](../plan.md), [impl/database/summary.md](../summary.md).
