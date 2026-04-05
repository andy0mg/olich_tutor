# Итерация: слой данных (iter-3-data-layer) — summary

**Tasklist:** [docs/tasks/tasklist-database.md](../../../tasklist-database.md)  
**Сводка области:** [docs/tasks/impl/database/summary.md](../summary.md)  
**План итерации:** [plan.md](./plan.md)

## Статус

| | |
|--|--|
| **Прогресс** | 3 из 5 задач завершены (01–03 ✅; 04–05 📋) |
| **Состояние итерации** | 🚧 В работе |

## Что сделано

- **Задача 01:** сценарии ученика и родителя, матрица «сценарий → сущности», требования к данным и связи родитель–ребёнок — [tasks/task-01-user-scenarios/summary.md](tasks/task-01-user-scenarios/summary.md).
- **Задача 02:** логическая и физическая модель в [docs/data-model.md](../../../../data-model.md), решения в [tasks/task-02-schema-design/](tasks/task-02-schema-design/), аудит по `postgresql-table-design`.
- **Задача 03:** [ADR-003](../../../../adr/adr-003-orm-migrations.md), [план и справка](tasks/task-03-tooling-adr/plan.md), обновлены [vision](../../../../vision.md) и [реестр ADR](../../../../adr/README.md).

## Следующие шаги

1. **Задача 04** — Docker PostgreSQL, `DATABASE_URL`, начальные миграции, Make-команды.
2. **Задача 05** — репозитории, PostgreSQL вместо `InMemoryApiStore`, тесты.

## Ключевые артефакты

| Артефакт | Где |
|----------|-----|
| Модель данных (логика + физика + ER) | [docs/data-model.md](../../../../data-model.md) |
| ADR по ORM и миграциям | [docs/adr/adr-003-orm-migrations.md](../../../../adr/adr-003-orm-migrations.md) |
| Планы и summary по задачам | [tasks/](tasks/) |

## Обновление документа

Дата последней актуализации: 2026-04-05 (план и сводка области — [impl/database/plan.md](../plan.md), [impl/database/summary.md](../summary.md)).
