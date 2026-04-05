# Область database: план итераций

**Tasklist:** [docs/tasks/tasklist-database.md](../../tasklist-database.md)

## Итерация `iter-3-data-layer` (завершена)

| | |
|--|--|
| **Статус** | ✅ Завершена (5 / 5 задач) |
| **Дата закрытия** | 2026-04-05 |
| **План (детальный)** | [iter-3-data-layer/plan.md](iter-3-data-layer/plan.md) |
| **Summary итерации** | [iter-3-data-layer/summary.md](iter-3-data-layer/summary.md) |
| **Сводка области** | [summary.md](summary.md) |
| **Дорожная карта** | итерация 3 «Персистентность и модель данных» в [docs/plan.md](../../../plan.md) |

### Цель итерации (кратко)

Ввести слой данных: сценарии и требования → логическая/физическая модель → ADR и инструменты (SQLAlchemy async, Alembic) → Docker PostgreSQL и миграции → ORM и интеграция API с БД вместо in-memory хранилища.

### Критерий завершения

Выполнен: все задачи 01–05 в tasklist — **Done**; проверки из раздела «Завершение итерации 3» в [tasklist-database.md](../../tasklist-database.md); артефакты и ссылки — в [iter-3-data-layer/summary.md](iter-3-data-layer/summary.md).

## Следующие итерации области

Новые итерации (например, расширение схемы, новые сущности под веб или отчёты) оформляются отдельной папкой `iter-N-…` рядом с `iter-3-data-layer` с собственными `plan.md` / `summary.md` и записями в [tasklist-database.md](../../tasklist-database.md).
