# Web Tasklist

## Обзор

Веб-клиент для ученика и родителя — SPA в каталоге `web/`, подключённый к единому REST API backend. Соответствует **итерации 4** дорожной карты ([plan.md](../plan.md)).

## Итерация `iter-4-web-client` (область web)

| | |
|--|--|
| **Статус** | ✅ Done |
| **Прогресс** | 7 / 7 задач |
| **План** | [impl/web/iter-4-web-client/plan.md](impl/web/iter-4-web-client/plan.md) |
| **Summary** | [impl/web/iter-4-web-client/summary.md](impl/web/iter-4-web-client/summary.md) |

## Легенда статусов

- 📋 **Planned** — запланирован
- 🚧 **In Progress** — в работе
- ✅ **Done** — завершён

## Связь с plan.md

| Этап (итерация) | Роль этого tasklist |
|-----------------|---------------------|
| **4 — Веб-клиент ученика и родителя** | Ведущая область: стек, scaffold, auth, экраны, интеграция. |
| **2 — MVP backend** | Предпосылка: API и сценарии реализованы ([tasklist-backend.md](tasklist-backend.md)). |
| **3 — Персистентность** | Предпосылка: данные в PostgreSQL ([tasklist-database.md](tasklist-database.md)). |

Опорные документы: [ADR-004: веб-стек](../adr/adr-004-web-stack.md), [vision.md](../vision.md), [data-model.md](../data-model.md), [backend/openapi.yaml](../../backend/openapi.yaml).

## Makefile

**Правило:** появились новые команды — добавь цель в **[Makefile](../../Makefile)** и отрази в [README.md](../../README.md) и [vision.md](../vision.md).

---

## Список задач

| № | Задача | Статус | Документы |
|---|--------|--------|-----------|
| 01 | Стек и каркас веб-клиента | ✅ Done | [план](impl/web/iter-4-web-client/tasks/task-01-scaffold/plan.md) \| [summary](impl/web/iter-4-web-client/tasks/task-01-scaffold/summary.md) |
| 02 | Аутентификация backend | ✅ Done | [план](impl/web/iter-4-web-client/tasks/task-02-backend-auth/plan.md) \| [summary](impl/web/iter-4-web-client/tasks/task-02-backend-auth/summary.md) |
| 03 | API для веб-сценариев | ✅ Done | [план](impl/web/iter-4-web-client/tasks/task-03-api-web/plan.md) \| [summary](impl/web/iter-4-web-client/tasks/task-03-api-web/summary.md) |
| 04 | Web: аутентификация и роутинг | ✅ Done | [план](impl/web/iter-4-web-client/tasks/task-04-web-auth/plan.md) \| [summary](impl/web/iter-4-web-client/tasks/task-04-web-auth/summary.md) |
| 05 | Web: экраны ученика | ✅ Done | [план](impl/web/iter-4-web-client/tasks/task-05-student-screens/plan.md) \| [summary](impl/web/iter-4-web-client/tasks/task-05-student-screens/summary.md) |
| 06 | Web: экраны родителя | ✅ Done | [план](impl/web/iter-4-web-client/tasks/task-06-parent-screens/plan.md) \| [summary](impl/web/iter-4-web-client/tasks/task-06-parent-screens/summary.md) |
| 07 | Интеграция, тесты, документация | ✅ Done | [план](impl/web/iter-4-web-client/tasks/task-07-integration/plan.md) \| [summary](impl/web/iter-4-web-client/tasks/task-07-integration/summary.md) |

---

## Задача 01: Стек и каркас веб-клиента ✅

### Цель

Зафиксировать веб-стек (ADR), создать каркас `web/` (Vite + React + TypeScript + Tailwind CSS), добавить Makefile-команды, обновить vision.md.

### Состав работ

- [x] ADR-004: выбор веб-стека
- [x] Scaffold `web/` через Vite (react-ts шаблон)
- [x] Установка зависимостей: Tailwind CSS, TanStack Query, React Router
- [x] Настройка Tailwind через Vite plugin
- [x] Структура каталогов: `src/api/`, `src/auth/`, `src/pages/`, `src/components/`
- [x] Makefile: `web-install`, `web-dev`, `web-build`, `web-lint`
- [x] Обновление vision.md (стек Web, Make-команды, структура репо)
- [x] Обновление ADR README

### Артефакты

- `web/` — каталог проекта с рабочим dev-сервером
- `docs/adr/adr-004-web-stack.md`
- Обновлённые: `Makefile`, `docs/vision.md`, `docs/adr/README.md`

---

## Задача 02: Аутентификация backend ✅

### Цель

JWT-инфраструктура на стороне backend: генерация и верификация токенов, таблица одноразовых кодов, эндпоинты auth, поддержка двойной схемы идентификации (заголовки для бота + Bearer JWT для веба), команда `/web` в Telegram-боте.

### Состав работ

- [x] Зависимости: PyJWT
- [x] Таблица `web_auth_codes` + миграция Alembic (002)
- [x] Сервис генерации/верификации JWT (access + refresh)
- [x] Эндпоинты: `POST /auth/login`, `POST /auth/refresh`, `GET /auth/me`, `POST /auth/accept-invite`, `POST /auth/web-code`, `POST /auth/invite-code`
- [x] Двойная идентификация: Bearer JWT + X-Channel/X-External-User-Id в deps.py
- [x] Команда `/web` и `/invite` в боте
- [x] Конфигурация: JWT_SECRET, JWT_ACCESS_EXPIRE_MINUTES, JWT_REFRESH_EXPIRE_DAYS, WEB_CODE_EXPIRE_MINUTES

---

## Задача 03: API для веб-сценариев ✅

### Цель

Backend-эндпоинты для веб-клиента: список диалогов, список снимков прогресса, родительские эндпоинты (invite, accept, children, activity, progress). Обновление OpenAPI.

### Состав работ

- [x] `GET /api/v1/conversations` — список диалогов текущего ученика
- [x] `GET /api/v1/knowledge-snapshots` — список снимков прогресса
- [x] `GET /api/v1/guardian-links/children` — список детей для родителя
- [x] `GET /api/v1/students/{student_id}/activity` — активность ребёнка
- [x] `GET /api/v1/students/{student_id}/progress` — прогресс ребёнка

---

## Задача 04: Web — аутентификация и роутинг ✅

### Цель

Страница входа, хранение JWT, auth context, защищённые маршруты, разделение по ролям (ученик/родитель).

### Состав работ

- [x] Страница входа (код из бота)
- [x] Страница принятия invite (родитель)
- [x] AuthContext: хранение user, login/logout, auto-refresh
- [x] RequireAuth guard с проверкой роли
- [x] Роутинг: студент (`/`, `/chat/:id`, `/progress`), родитель (`/parent`, `/parent/child/:id/*`)

---

## Задача 05: Web — экраны ученика ✅

### Цель

Список диалогов, чат-интерфейс (просмотр + отправка), дашборд прогресса. Интеграция с реальным API.

---

## Задача 06: Web — экраны родителя ✅

### Цель

Выбор ребёнка, обзор активности, прогресс ребёнка. Интеграция с реальным API.

---

## Задача 07: Интеграция, тесты, документация ✅

### Цель

E2E проверка полного цикла (бот -> код -> веб); обновление README, vision.md, OpenAPI; deploy-настройки.
