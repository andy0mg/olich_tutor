# Задача 03: выбор инструментов миграций и доступа к БД — summary

## Статус

Завершена.

## Что сделано

- Принят **[ADR-003: доступ к БД и миграции](../../../../../adr/adr-003-orm-migrations.md)** — SQLAlchemy 2.0 async, драйвер **asyncpg**, миграции **Alembic**; таблица альтернатив (Tortoise, `databases`, только asyncpg) и последствия для репозитория.
- **[План и практическая справка](plan.md)** — зависимости, целевая структура `backend/alembic/`, `backend/db/` (модели, сессия), команды `revision` / `upgrade` / `downgrade`, напоминание про проверку на PostgreSQL.
- Обновлены **[docs/vision.md](../../../../../vision.md)** (стек: sqlalchemy, asyncpg, alembic, greenlet; архитектурные решения — ссылка на ADR-003) и **[docs/adr/README.md](../../../../../adr/README.md)** (реестр).

## Не входило в задачу

- Установка пакетов в `requirements.txt`, Docker, `DATABASE_URL`, Makefile — **задача 04**.
- Код моделей и репозиториев — **задача 05**.

Дата: 2026-04-05.
