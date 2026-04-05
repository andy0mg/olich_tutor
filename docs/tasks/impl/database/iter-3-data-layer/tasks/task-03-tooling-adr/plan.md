# Задача 03: выбор инструментов миграций и доступа к БД — план

**Tasklist:** [docs/tasks/tasklist-database.md](../../../../../tasks/tasklist-database.md)  
**ADR:** [docs/adr/adr-003-orm-migrations.md](../../../../../adr/adr-003-orm-migrations.md)

## Цель

Зафиксировать ORM, драйвер и инструмент миграций; дать разработчикам практическую справку до появления кода и Make-целей в задаче 04.

## Состав работ (чеклист)

- [x] Сравнение вариантов — в [ADR-003](../../../../../adr/adr-003-orm-migrations.md)
- [x] ADR-003 принят
- [x] Практическая справка — этот файл, раздел ниже
- [x] [docs/vision.md](../../../../../vision.md) — стек и ссылка на ADR-003
- [x] [docs/adr/README.md](../../../../../adr/README.md) — реестр

---

## Практическая справка по стеку (SQLAlchemy 2 async + Alembic + asyncpg)

### Зависимости (будут добавлены в `requirements.txt` в задаче 04)

| Пакет | Назначение |
|---|---|
| `sqlalchemy[asyncio]` | ORM 2.0, async engine и сессии |
| `asyncpg` | Асинхронный драйвер PostgreSQL |
| `alembic` | Миграции схемы |
| `greenlet` | Требование SQLAlchemy для части async-паттернов |

Опционально для dev с SQLite (если включат в проект): `aiosqlite` — только при соблюдении переносимости типов ([ADR-001](../../../../../adr/adr-001-database.md)).

### Целевая структура каталогов (задача 04–05)

Размещение — под **`backend/`**, в духе [vision](../../../../../vision.md):

```
backend/
├── alembic.ini              # точка входа Alembic (путь к ревизиям — env.py)
├── alembic/
│   ├── env.py                 # подключение AsyncEngine, target_metadata
│   └── versions/              # файлы ревизий YYYY_MM_DD_hhmm_<slug>.py
├── db/                        # или другое согласованное имя
│   ├── __init__.py
│   ├── session.py             # async_engine, async_sessionmaker, get_session
│   └── models/                # DeclarativeBase, модели таблиц
│       └── __init__.py
```

Точные имена модулей (`db` vs `infrastructure/db`) задаются при реализации; важно: **один** `DeclarativeBase` и **один** `MetaData` для `target_metadata` в Alembic.

### Модель (ORM)

- Базовый класс: `DeclarativeBase` (SQLAlchemy 2).
- Таблицы и колонки: `Mapped[...]`, `mapped_column`, имена в **`snake_case`**, как в [data-model.md](../../../../../data-model.md).
- Связи: `relationship` с явными `foreign_keys` там, где нужно избежать неоднозначности.

Детальная реализация моделей и репозиториев — **задача 05**.

### Сессия и FastAPI (паттерн)

- Создать `async_engine` из `DATABASE_URL` (PostgreSQL: `postgresql+asyncpg://...`).
- `async_sessionmaker(engine, expire_on_commit=False)` — типичные настройки для API.
- В обработчиках: зависимость `Depends`, которая открывает `AsyncSession`, выполняет работу в `async with session`, делает `commit` при успехе; либо выдаёт сессию как контекст — конкретная схема фиксируется в коде задачи 05.

### Команды Alembic (после инициализации в задаче 04)

Из корня репозитория (или с `-c backend/alembic.ini`), с активированным venv:

```bash
# новая ревизия с автогенерацией по моделям (после изменения ORM)
alembic revision --autogenerate -m "описание изменения"

# применить все миграции
alembic upgrade head

# откатить одну ревизию
alembic downgrade -1

# откатить до конкретной ревизии
alembic downgrade <revision_id>
```

В проекте ожидается обёртка в **Makefile** (`make db-migrate` и т.д.) в задаче 04.

### Что проверить перед продом

- `alembic upgrade head` на чистой БД PostgreSQL.
- Нет ли в миграциях конструкций, специфичных только для SQLite, если SQLite использовался локально.
- Соответствие физической схемы [data-model.md](../../../../../data-model.md).

---

## Definition of Done

- [x] ADR-003 и справка согласованы с async + PostgreSQL
- [x] vision и реестр ADR обновлены
