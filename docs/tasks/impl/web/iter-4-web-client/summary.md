# Итерация 4: Веб-клиент ученика и родителя — summary

**Статус:** ✅ Done

## Что сделано

### Инфраструктура
- **ADR-004:** зафиксирован веб-стек (React 19 + Vite + TypeScript + Tailwind CSS + TanStack Query + React Router)
- **web/** scaffold: Vite react-ts шаблон, все зависимости установлены, Tailwind через Vite plugin, proxy `/api` на backend
- **Makefile:** `web-install`, `web-dev`, `web-build`, `web-lint`

### Backend: аутентификация
- PyJWT, таблица `web_auth_codes` (миграция 002), JWT-сервис (access + refresh)
- Auth-эндпоинты: `/auth/login`, `/auth/refresh`, `/auth/me`, `/auth/web-code`, `/auth/invite-code`, `/auth/accept-invite`
- Двойная идентификация: Bearer JWT (веб) + X-Channel/X-External-User-Id (бот)
- Команды бота: `/web` (код для входа), `/invite` (код для родителя)

### Backend: API для веб-сценариев
- `GET /conversations` — список диалогов ученика
- `GET /knowledge-snapshots` — список снимков прогресса
- Guardian-links router: `GET /guardian-links/children`, `GET /students/{id}/activity`, `GET /students/{id}/progress`

### Web: аутентификация и роутинг
- LoginPage (ввод кода), InvitePage (принятие приглашения)
- AuthContext с login/acceptInvite/logout, auto-refresh JWT
- RequireAuth guard с проверкой роли
- Маршруты: студент (/, /chat/:id, /progress), родитель (/parent, /parent/child/:id/*)

### Web: экраны ученика
- ConversationsPage: список диалогов с датами
- ChatPage: история + отправка сообщений + typing indicator
- ProgressPage: таблица KnowledgeSnapshot с LevelBadge

### Web: экраны родителя
- ChildrenPage: карточки детей с ссылками
- ChildActivityPage: статистика + последние занятия
- ChildProgressPage: таблица снимков прогресса

### Интеграция и документация
- TypeScript — clean build, ruff — all pass
- README обновлён (статусы, Make-команды, раздел «Веб-клиент»)
- vision.md обновлён (стек Web, Make-команды, структура репо)
- .gitignore, .env.example обновлены

## Артефакты

| Что | Где |
|-----|-----|
| ADR веб-стека | `docs/adr/adr-004-web-stack.md` |
| Миграция auth | `backend/alembic/versions/002_web_auth_codes.py` |
| JWT-сервис | `backend/services/jwt_service.py` |
| Auth-сервис | `backend/services/auth_service.py` |
| Auth-роутер | `backend/api/routers/v1/auth.py` |
| Guardian-links роутер | `backend/api/routers/v1/guardian_links.py` |
| Веб-клиент | `web/` |
| Tasklist | `docs/tasks/tasklist-web.md` |
