# Database Tasklist

## Обзор

Внедрение полноценного слоя данных: от пользовательских сценариев и проектирования схемы до замены in-memory хранения на PostgreSQL. Соответствует **итерации 3** дорожной карты ([plan.md](../plan.md)) — «Персистентность и модель данных».

## Итерация `iter-3-data-layer` (область database)

| | |
|--|--|
| **Статус** | 🚧 In Progress |
| **Прогресс** | 4 / 5 задач (01–04 ✅; 05 📋) |
| **План** | [impl/database/plan.md](impl/database/plan.md) · [iter-3-data-layer/plan.md](impl/database/iter-3-data-layer/plan.md) |
| **Summary** | [impl/database/summary.md](impl/database/summary.md) · [iter-3-data-layer/summary.md](impl/database/iter-3-data-layer/summary.md) |

## Легенда статусов

- 📋 **Planned** — запланирован
- 🚧 **In Progress** — в работе
- ✅ **Done** — завершён

## Связь с plan.md

| Этап (итерация) | Роль этого tasklist |
|-----------------|---------------------|
| **3 — Персистентность и модель данных** | Ведущая область: сценарии → схема → инструменты → инфраструктура → интеграция. Детализирует задачу 09 из [tasklist-backend.md](tasklist-backend.md). |
| **2 — MVP-учебные сценарии** | Предпосылка: API и сценарии в памяти ([tasklist-backend.md](tasklist-backend.md), задачи 01–08) завершены. |
| **4 — Веб-клиент** | Данные и связи, заложенные здесь, покрывают будущие потребности frontend ([tasklist-web.md](tasklist-web.md)). |

Опорные документы: [ADR-001: выбор СУБД](../adr/adr-001-database.md), [ADR-003: ORM и миграции](../adr/adr-003-orm-migrations.md), [data-model.md](../data-model.md), [vision.md](../vision.md), [idea.md](../idea.md).

## Skills

При проектировании схемы и ревью таблиц — skill **`postgresql-table-design`**. При выборе ORM/миграций и реализации — **`modern-python`**, **`fastapi-templates`**, **`async-python-patterns`** по смыслу задачи.

## Makefile

**Правило:** появились новые команды запуска, миграций или обслуживания БД — добавь цель в **[Makefile](../../Makefile)** и отрази в [README.md](../../README.md) и [vision.md](../vision.md) (раздел Make-команд).

---

## Список задач

| № | Задача | Статус | Документы |
|---|--------|--------|-----------|
| 01 | Сценарии пользователя и требования к данным | ✅ Done | [план](impl/database/iter-3-data-layer/tasks/task-01-user-scenarios/plan.md) \| [summary](impl/database/iter-3-data-layer/tasks/task-01-user-scenarios/summary.md) |
| 02 | Проектирование схемы данных | ✅ Done | [план](impl/database/iter-3-data-layer/tasks/task-02-schema-design/plan.md) \| [summary](impl/database/iter-3-data-layer/tasks/task-02-schema-design/summary.md) |
| 03 | Выбор инструментов миграций и доступа к БД | ✅ Done | [план](impl/database/iter-3-data-layer/tasks/task-03-tooling-adr/plan.md) \| [summary](impl/database/iter-3-data-layer/tasks/task-03-tooling-adr/summary.md) |
| 04 | Инфраструктура БД | ✅ Done | [план](impl/database/iter-3-data-layer/tasks/task-04-db-infra/plan.md) \| [summary](impl/database/iter-3-data-layer/tasks/task-04-db-infra/summary.md) |
| 05 | ORM-модели, репозитории и интеграция в backend | 📋 Planned | [план](impl/database/iter-3-data-layer/tasks/task-05-orm-integration/plan.md) \| [summary](impl/database/iter-3-data-layer/tasks/task-05-orm-integration/summary.md) |

---

## Актуализация проектной документации (по задачам)

| Файл | 01 Сценарии | 02 Схема | 03 Инструменты | 04 Инфра | 05 Интеграция |
|------|:-----------:|:--------:|:--------------:|:--------:|:-------------:|
| [docs/vision.md](../vision.md) | ○ | ○ | ● | ● | ● |
| [docs/data-model.md](../data-model.md) | ○ | ● | ○ | ○ | ● |
| [docs/adr/README.md](../adr/README.md) | ○ | ○ | ● | ○ | ○ |
| [README.md](../../README.md) | ○ | ○ | ○ | ● | ● |
| [.env.example](../../.env.example) | ○ | ○ | ○ | ● | ○ |
| [backend/.env.example](../../backend/.env.example) | ○ | ○ | ○ | ● | ○ |
| [Makefile](../../Makefile) | ○ | ○ | ○ | ● | ○ |

● — обычно требуется правка · ○ — по необходимости.

---

## Задача 01: Сценарии пользователя и требования к данным ✅

### Цель

Описать базовые сценарии ученика и родителя без глубоких технических подробностей; вывести из них требования к данным и связям, чтобы заложить основу под схему БД и будущий frontend.

### Состав работ

- [x] Сценарии ученика: диалог с репетитором, получение задания, просмотр истории занятий, просмотр прогресса по темам
- [x] Сценарии родителя: просмотр активности ребёнка, результаты и динамика по темам, видимость слабых мест
- [x] Матрица «сценарий → сущности и связи» — какие данные и отношения из [data-model.md](../data-model.md) задействует каждый сценарий
- [x] Фиксация требований к данным в plan.md задачи (или отдельном документе в папке задачи)

### Артефакты

- `docs/tasks/impl/database/iter-3-data-layer/tasks/task-01-user-scenarios/plan.md` — сценарии, матрица, требования к данным

### Definition of Done

**Агент:**
- Сценарии покрывают роли ученика и родителя
- Каждый сценарий ссылается на конкретные сущности из [data-model.md](../data-model.md)
- Нет сценария, для которого не определены нужные данные
- Матрица показывает, какие связи обязательны, а какие — на перспективу

**Пользователь:**
- Открыть plan.md задачи, убедиться что сценарии соответствуют продуктовому видению из [idea.md](../idea.md) и [vision.md](../vision.md)
- Проверить, что сценарии родителя дают понятную картину: что именно родитель увидит о ребёнке

### Документы

- 📋 [План](impl/database/iter-3-data-layer/tasks/task-01-user-scenarios/plan.md)
- 📝 [Summary](impl/database/iter-3-data-layer/tasks/task-01-user-scenarios/summary.md)

---

## Задача 02: Проектирование схемы данных ✅

### Цель

Актуализировать логическую модель, спроектировать физическую модель (таблицы, типы PostgreSQL, индексы, ограничения) и нарисовать физическую ER-диаграмму. Ревью схемы через skill `postgresql-table-design`.

### Состав работ

- [x] Актуализировать [docs/data-model.md](../data-model.md) по итогам задачи 01 (новые сущности или поля, если выявлены)
- [x] Спроектировать физическую схему: таблицы, колонки, типы PostgreSQL, PK/FK, уникальные ограничения, индексы
- [x] Нарисовать физическую ER-диаграмму (Mermaid) — добавить в `docs/data-model.md` или в отдельный файл рядом
- [x] Провести ревью схемы по чеклисту skill `postgresql-table-design`: типы данных (`TIMESTAMPTZ`, `TEXT`, `BIGINT GENERATED ALWAYS AS IDENTITY` / UUID), индексы на FK, `NOT NULL` / `DEFAULT`, нормализация до 3NF, JSONB — только обоснованно
- [x] Зафиксировать физическую секцию в `docs/data-model.md`

### Артефакты

- Обновлённый `docs/data-model.md` (логическая + физическая модель, ER-диаграмма)
- `docs/tasks/impl/database/iter-3-data-layer/tasks/task-02-schema-design/plan.md`

### Definition of Done

**Агент:**
- Физическая схема покрывает все сущности из data-model
- ER-диаграмма отражает FK и кардинальности
- Чеклист `postgresql-table-design` пройден без критичных замечаний
- Нет типов, которые ломают переносимость между dev-SQLite и prod-PostgreSQL (если SQLite для dev сохраняется)

**Пользователь:**
- Открыть `docs/data-model.md` — есть и логическая, и физическая модель
- ER-диаграмма рендерится в Markdown-просмотрщике
- Таблицы, типы и индексы выглядят адекватно для описанных сценариев

### Документы

- 📋 [План](impl/database/iter-3-data-layer/tasks/task-02-schema-design/plan.md)
- 📝 [Summary](impl/database/iter-3-data-layer/tasks/task-02-schema-design/summary.md)

---

## Задача 03: Выбор инструментов миграций и доступа к БД ✅

### Цель

Обоснованно выбрать ORM / query builder и инструмент миграций; зафиксировать ADR с обоснованием; подготовить практическую справку по использованию в проекте.

### Состав работ

- [x] Сравнить варианты: SQLAlchemy 2.0 (async) + Alembic, альтернативы (Tortoise ORM, databases + encode/databases, raw asyncpg и т.д.)
- [x] Подготовить ADR (например `docs/adr/adr-003-orm-migrations.md`): контекст, решение, обоснование, последствия
- [x] Написать практическую справку: как устроен выбранный инструмент, структура файлов в проекте, ключевые команды, паттерны использования
- [x] Обновить [docs/vision.md](../vision.md) (раздел «Технологический стек» — новые пакеты)
- [x] Обновить [docs/adr/README.md](../adr/README.md) (добавить ссылку на новый ADR)

### Артефакты

- `docs/adr/adr-003-orm-migrations.md` (или следующий свободный номер)
- Практическая справка — в plan.md задачи или отдельным файлом в папке задачи

### Definition of Done

**Агент:**
- ADR зафиксирован, ссылается из `docs/adr/README.md` и `docs/vision.md`
- Практическая справка отвечает на вопросы: как создать модель, как создать и применить миграцию, как откатить
- Выбранный инструмент совместим с async-стеком (FastAPI + Uvicorn) и PostgreSQL как целевой СУБД

**Пользователь:**
- Прочитать ADR — понятно, что выбрано и почему
- Справка отвечает на «как мне создать миграцию / модель» без дополнительного гугления

### Документы

- ✅ [План](impl/database/iter-3-data-layer/tasks/task-03-tooling-adr/plan.md)
- ✅ [Summary](impl/database/iter-3-data-layer/tasks/task-03-tooling-adr/summary.md)

---

## Задача 04: Инфраструктура БД ✅

### Цель

Запуск PostgreSQL локально, создание начальных миграций по физической схеме, команды для управления окружением и просмотра данных.

### Состав работ

- [x] Docker Compose для PostgreSQL (новый `docker-compose.yml` или секция в существующем)
- [x] Конфигурация: `DATABASE_URL` в `.env.example` (корень и `backend/`), расширение `backend/config.py` (`Settings`)
- [x] Начальные миграции по физической схеме из задачи 02
- [x] Make-команды: `db-up` (запуск), `db-down` (остановка), `db-reset` (пересоздание с нуля), `db-migrate` (применить миграции), `db-shell` (psql к локальной БД)
- [x] Проверка: миграции на чистой БД без ошибок; пересоздание окружения
- [x] Обновить [README.md](../../README.md) (раздел «Запуск»), [docs/vision.md](../vision.md) (раздел Make-команд), `.env.example`

### Артефакты

- `docker-compose.yml`
- Каталог миграций (путь зависит от выбора инструмента в задаче 03)
- Обновлённые: `.env.example`, `backend/.env.example`, `backend/config.py`, `Makefile`, `README.md`, `docs/vision.md`

### Definition of Done

**Агент:**
- `make db-up && make db-migrate` на чистом окружении проходит без ошибок
- Таблицы в БД соответствуют физической схеме из задачи 02
- `make db-reset` пересоздаёт БД с нуля и повторно применяет миграции
- Переменные окружения документированы в `.env.example`

**Пользователь:**
- Выполнить `make db-up` — контейнер PostgreSQL запущен
- Выполнить `make db-migrate` — миграции применены
- Выполнить `make db-shell` — подключение к БД, таблицы видны через `\dt`
- Выполнить `make db-reset` — БД пересоздана

### Документы

- ✅ [План](impl/database/iter-3-data-layer/tasks/task-04-db-infra/plan.md)
- ✅ [Summary](impl/database/iter-3-data-layer/tasks/task-04-db-infra/summary.md)

---

## Задача 05: ORM-модели, репозитории и интеграция в backend 📋

### Цель

Заменить `InMemoryApiStore` на PostgreSQL; сценарии итерации 2 (вопрос к репетитору, фиксация ДЗ) работают с БД и переживают перезапуск backend.

### Состав работ

- [ ] ORM-модели по физической схеме (инструмент — по результатам задачи 03)
- [ ] Слой репозиториев: абстракция (протокол / ABC) + реализация для PostgreSQL
- [ ] Интеграция в FastAPI: DI (`Depends`), управление сессиями и транзакциями
- [ ] Адаптация существующих API-тестов (`tests/api/`) для работы с БД (или тестовый in-memory fallback)
- [ ] Тесты репозиториев (или контрактные тесты с миграциями)
- [ ] Проверка: перезапуск backend — диалоги и прогресс на месте
- [ ] Удаление или деактивация `InMemoryApiStore` (при необходимости — оставить как fallback для быстрых тестов)
- [ ] Обновить `docs/data-model.md` (секция «Соответствие полей HTTP API v1» — при изменениях)
- [ ] Обновить [README.md](../../README.md) (запуск с БД: `make db-up && make db-migrate && make run-backend`)

### Артефакты

- Модули в `backend/`: models (ORM), repositories, db session / engine
- Тесты: `tests/` — репозитории и/или обновлённые API-тесты
- Обновлённые: `docs/data-model.md`, `README.md`

### Definition of Done

**Агент:**
- `make test` зелёный
- Сценарии «вопрос к репетитору» и «фиксация ДЗ» через API работают с PostgreSQL
- После перезапуска `make run-backend` (стоп → старт) данные сохраняются
- Нет дублирования доменной логики между `InMemoryApiStore` и репозиториями
- OpenAPI (`backend/openapi.yaml`) не сломан; существующие контракты совместимы

**Пользователь:**
- Запустить `make db-up && make db-migrate && make run-backend`
- Выполнить сценарии через бот или curl (создать диалог, отправить сообщение, зафиксировать прогресс)
- Перезапустить backend (`Ctrl+C`, `make run-backend`)
- Убедиться, что диалоги и прогресс на месте (GET диалога, проверка в `make db-shell`)

### Документы

- 📋 [План](impl/database/iter-3-data-layer/tasks/task-05-orm-integration/plan.md)
- 📝 [Summary](impl/database/iter-3-data-layer/tasks/task-05-orm-integration/summary.md)

---

## Завершение итерации 3

| | |
|--|--|
| **Агент проверяет** | Все задачи 01–05 завершены; `make test` зелёный; миграции на чистой БД проходят; API работает с PostgreSQL; данные переживают рестарт. |
| **Пользователь проверяет** | `make db-up && make db-migrate && make run-backend`; ручной прогон сценариев в Telegram или curl; перезапуск — данные на месте; `make db-shell` — таблицы и записи видны. |
| **Команды** | `make install`, `make db-up`, `make db-migrate`, `make db-reset`, `make db-shell`, `make run-backend`, `make test`, `make check`. |
| **Где смотреть результат** | Таблицы в PostgreSQL; ответы API; логи backend; документация (`README`, `vision`, `data-model`). |
