# Итерация: слой данных (iter-3-data-layer)

**Область:** database — входная точка планов: [docs/tasks/impl/database/plan.md](../plan.md)  
**Tasklist:** [docs/tasks/tasklist-database.md](../../../tasklist-database.md)  
**Дорожная карта:** итерация 3 «Персистентность и модель данных» в [docs/plan.md](../../../../plan.md).

## Цель итерации

Ввести полноценный слой данных: от продуктовых сценариев и **логической/физической модели** до **PostgreSQL**, инструментов миграций/ORM и **интеграции backend** вместо in-memory хранения.

## Ценность

- Данные переживают перезапуск процессов; единая модель для бота, API и будущего веб-клиента.
- Схема и документация согласованы с [docs/data-model.md](../../../../data-model.md) и [ADR-001](../../../../adr/adr-001-database.md).

## Состав и порядок задач

| № | Задача | Статус на момент плана | Папка |
|---|--------|------------------------|-------|
| 01 | Сценарии пользователя и требования к данным | ✅ Done | [tasks/task-01-user-scenarios/](tasks/task-01-user-scenarios/) |
| 02 | Проектирование схемы данных | ✅ Done | [tasks/task-02-schema-design/](tasks/task-02-schema-design/) |
| 03 | Выбор инструментов миграций и доступа к БД | ✅ Done | [tasks/task-03-tooling-adr/](tasks/task-03-tooling-adr/) |
| 04 | Инфраструктура БД | ✅ Done | [tasks/task-04-db-infra/](tasks/task-04-db-infra/) |
| 05 | ORM-модели, репозитории и интеграция в backend | ✅ Done | [tasks/task-05-orm-integration/](tasks/task-05-orm-integration/) |

## Опорные документы

- [docs/data-model.md](../../../../data-model.md)
- [docs/vision.md](../../../../vision.md)
- [docs/adr/adr-001-database.md](../../../../adr/adr-001-database.md)
- [docs/adr/adr-003-orm-migrations.md](../../../../adr/adr-003-orm-migrations.md)
- Связь с backend: [tasklist-backend.md](../../../tasklist-backend.md) (задача 09 и контекст итерации 2)

## Критерий завершения итерации

Все задачи 01–05 в [tasklist-database.md](../../../tasklist-database.md) отмечены как **Done**; выполнены проверки из раздела «Завершение итерации 3» в tasklist.
