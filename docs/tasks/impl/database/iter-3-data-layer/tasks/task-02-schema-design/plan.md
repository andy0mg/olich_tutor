# Задача 02: проектирование схемы данных — план и решения

**Итерация:** iter-3-data-layer  
**Tasklist:** [docs/tasks/tasklist-database.md](../../../../../tasklist-database.md)  
**Вход:** [task-01 plan](../task-01-user-scenarios/plan.md), [docs/data-model.md](../../../../../../data-model.md)

## Цель

Зафиксировать логические дополнения по задаче 01, спроектировать физическую модель PostgreSQL и отразить её в [docs/data-model.md](../../../../../../data-model.md).

## Решения по модели

### 1. Идентификаторы и API v1

| Область | Решение |
|--------|---------|
| Публичные id в HTTP API (`Conversation`, `Message`, `KnowledgeSnapshot`, `Enrollment`, `LearningStream` в OpenAPI) | Первичный ключ в БД — **`UUID`** (`gen_random_uuid()`), тот же id отдаётся в JSON. |
| Учётные записи и профиль ученика | Внутренние суррогатные ключи **`BIGINT GENERATED ALWAYS AS IDENTITY`** (`users`, `students`). В API v1 ученик не идентифицируется внутренним id — резолв по `(channel, external_user_id)`. |
| Связь родитель–ребёнок | Таблица `guardian_student_links`: PK **`BIGINT GENERATED ALWAYS AS IDENTITY`**. В API для родителя пока нет контракта — внутренний id допустим до появления ресурсов. |

### 2. Идентификация пользователя по каналу

- Таблица **`user_channel_identities`**: связь `user_id` → пара **`(channel, external_user_id)`** с ограничением **`UNIQUE (channel, external_user_id)`**.
- Один **User** может иметь несколько идентичностей (например Telegram и web) — отдельные строки.

### 3. Роли ученика и родителя

- Наличие строки в **`students`** с `user_id` задаёт профиль ученика (роль «ученик» на уровне данных).
- Роль «родитель» подтверждается участием в **`guardian_student_links`** как `parent_user_id`; отдельная таблица ролей на MVP не вводится.

### 4. Связь родитель ↔ ученик (M:N)

- Таблица **`guardian_student_links`**: `parent_user_id` → `users`, `student_id` → `students`, **`status`** (`pending` \| `active` \| `rejected` \| `revoked` \| `expired`), аудит `created_at`, `updated_at`.
- **Повторное приглашение** после `rejected` / `revoked`: новая строка (история попыток сохраняется).
- **Не более одной активной** связи на пару `(parent_user_id, student_id)`: частичный уникальный индекс **`UNIQUE (parent_user_id, student_id) WHERE status = 'active'`** (PostgreSQL).
- **Не более одной ожидающей** приглашённой связи на ту же пару: **`UNIQUE (parent_user_id, student_id) WHERE status = 'pending'`** — чтобы не плодить параллельные pending.

### 5. Приглашение (токен и срок)

- **Вариант:** поля приглашения **в той же таблице** `guardian_student_links`: `invite_token_hash` (**TEXT**, **UNIQUE** там, где не NULL), `expires_at` (**TIMESTAMPTZ**, NULL после принятия или отмены). В хранилище — **хэш** токена (не сырое значение), см. раздел безопасности в реализации.
- **Обоснование:** одна сущность «попытка установить связь»; запрос по токену — редкий путь, достаточно индекса на `invite_token_hash`; отдельная таблица не даёт выигрыша для MVP данных.

### 6. Перечисления (статусы, каналы, роли сообщений)

- В физической схеме: **`TEXT`** + **`CHECK`** (переносимо с SQLite; без `CREATE TYPE ... AS ENUM` в MVP схемы).

### 7. Метаданные сообщений

- Опциональная колонка **`metadata JSONB`** в `messages` — только для служебных полей (модель, токены); без индексов на JSONB до появления запросов (чеклист skill).

### 8. Переносимость PostgreSQL / SQLite

- Зафиксировано в [docs/data-model.md](../../../../../../data-model.md) (раздел «Переносимость»): целевая СУБД — PostgreSQL; локальная разработка после задачи 04 — **PostgreSQL в Docker**. Схема описана на PostgreSQL; частичные уникальные индексы и `JSONB` при использовании SQLite в dev потребуют упрощений или отдельной ветки миграций — **не цель** текущей задачи.

## Соответствие «сущность → таблица»

| Логическая сущность | Таблица |
|----------------------|---------|
| User | `users` |
| Идентификация по каналу | `user_channel_identities` |
| Student | `students` |
| LearningStream | `learning_streams` |
| Enrollment | `enrollments` |
| Conversation | `conversations` |
| Message | `messages` |
| KnowledgeSnapshot | `knowledge_snapshots` |
| Связь родитель–ребёнок (и жизненный цикл приглашения) | `guardian_student_links` |

## Ревью: postgresql-table-design

Проверено по [.agents/skills/postgresql-table-design/SKILL.md](../../../../../../.agents/skills/postgresql-table-design/SKILL.md):

| Критерий | Результат |
|----------|-----------|
| PK для ссылочных сущностей | Да: `BIGINT IDENTITY` / `UUID` по смыслу |
| `TIMESTAMPTZ`, `TEXT`, избегать `timestamp` без TZ | Да |
| Индексы на FK | Заданы в data-model |
| `NOT NULL` / `DEFAULT` где уместно | Задано в описании колонок |
| Нормализация до 3NF | Да; JSONB только для опциональных метаданных сообщения |
| FK: явные `ON DELETE` | Указаны в data-model |

**Критичных замечаний нет.**

## Открытые вопросы (вне объёма схемы 02)

- Эндпоинты API для родителя и приглашений — следующие задачи backend.
- Детальная политика отзыва связи и уведомления — продукт/UX.

## Связанные документы

- [docs/data-model.md](../../../../../../data-model.md)
- [docs/adr/adr-001-database.md](../../../../../../adr/adr-001-database.md)
- [backend/openapi.yaml](../../../../../../../backend/openapi.yaml)
