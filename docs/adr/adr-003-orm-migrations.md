# ADR-003: доступ к БД и миграции (SQLAlchemy 2 async + Alembic)

| Поле | Значение |
|---|---|
| Статус | Принято |
| Дата | 2026-04-05 |
| Контекст | [ADR-001](adr-001-database.md), [ADR-002](adr-002-rest-backend.md), [data-model.md](../data-model.md), [tasklist-database.md](../tasks/tasklist-database.md) |

## Контекст

Backend работает как **async** ASGI-приложение (FastAPI + Uvicorn, [ADR-002](adr-002-rest-backend.md)). Целевая СУБД — **PostgreSQL**; для dev/раннего MVP допустим SQLite при переносимых миграциях ([ADR-001](adr-001-database.md)). Физическая схема таблиц задана в [data-model.md](../data-model.md) (итерация 3, задача 02). Предстоит слой репозиториев и замена in-memory хранилища на персистентность (задача 05).

Нужно зафиксировать стек **доступа к данным** и **версионирования схемы**, совместимый с async-стеком и PostgreSQL, без привязки к конкретным версиям пакетов в этом документе (версии задаются в `requirements.txt` при внедрении).

## Решение

1. **ORM — SQLAlchemy 2.0** в режиме **async**: `AsyncEngine`, `async_sessionmaker`, `AsyncSession`, декларативные модели (Mapped, mapped_column).

2. **Драйвер PostgreSQL — asyncpg** (через URL `postgresql+asyncpg://...`). Для сценария SQLite в dev — `aiosqlite` и URL `sqlite+aiosqlite/...`, только если типы и миграции остаются переносимыми ([ADR-001](adr-001-database.md)).

3. **Миграции — Alembic**, конфигурация привязана к метаданным моделей SQLAlchemy; ревизии в репозитории, применение через CLI (в Makefile — в задаче инфраструктуры 04).

4. Зависимость **`greenlet`** требуется для части async-паттернов SQLAlchemy 2 — добавляется вместе с SQLAlchemy при внедрении.

## Обоснование

- Единый стиль **async** с FastAPI и Uvicorn: запросы к БД не блокируют event loop при типичном I/O.
- **PostgreSQL** — полная поддержка типов из физической модели (в т.ч. JSONB, `TIMESTAMPTZ`, `CHECK`).
- **Alembic** — зрелый инструмент миграций для SQLAlchemy: автогенерация по diff моделей, линейная история `upgrade` / `downgrade`, привычный workflow для команд.
- Один язык описания схемы (Python-модели) для ORM и для автогенерации миграций снижает расхождение с [data-model.md](../data-model.md).

## Рассмотренные альтернативы

| Альтернатива | Плюсы | Минусы | Почему не выбрано как основа |
|---|---|---|---|
| **Tortoise ORM + Aerich** | Простой onboarding для async | Другая экосистема, миграции не Alembic; меньше примеров под DDD/репозитории в связке с FastAPI | Дублирование знаний; слабее связка «модель ↔ Alembic» относительно SQLAlchemy |
| **`databases` + SQLAlchemy Core / raw SQL** | Гибкость, тонкий слой | Больше ручного SQL и дублирования при ~10 связанных сущностях | Выше стоимость сопровождения MVP без выигрыша в скорости разработки |
| **Только asyncpg (без ORM)** | Максимальный контроль и производительность запросов | Две правды: документ data-model и ручные запросы/маппинг | Риск рассинхрона схемы и домена; ORM окупается на объёме таблиц и связей проекта |
| **Синхронный SQLAlchemy + thread pool** | Привычные паттерны sync | Смешение стилей с async FastAPI, лишняя сложность с пулом потоков | Несоответствие выбранному async REST-слою |

## Последствия

- В `requirements.txt` появятся пакеты вида: `sqlalchemy[asyncio]`, `asyncpg`, `alembic`, `greenlet` (точные версии — при задаче инфраструктуры и интеграции).
- Каталог миграций и `alembic.ini` размещаются под **`backend/`** (целевая структура — в [практической справке задачи 03](../tasks/impl/database/iter-3-data-layer/tasks/task-03-tooling-adr/plan.md)); ORM-модели — в отдельных модулях `backend/`, без дублирования бизнес-логики в клиентах.
- Перед выкладкой в прод **обязательна** проверка миграций на PostgreSQL; использование SQLite в CI/dev не отменяет проверки на целевой СУБД ([ADR-001](adr-001-database.md)).
- Смена ORM или инструмента миграций — новый ADR; текущий ADR остаётся в истории.

## Связанные документы

- [ADR-001: выбор СУБД](adr-001-database.md)
- [ADR-002: REST-слой backend](adr-002-rest-backend.md)
- [data-model.md](../data-model.md)
- [docs/tasks/tasklist-database.md](../tasks/tasklist-database.md)
- Практическая справка: [task-03-tooling-adr/plan.md](../tasks/impl/database/iter-3-data-layer/tasks/task-03-tooling-adr/plan.md)
