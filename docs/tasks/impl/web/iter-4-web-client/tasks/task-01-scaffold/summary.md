# Задача 01: Стек и каркас веб-клиента — summary

**Статус:** ✅ Done

## Что сделано

- ADR-004 создан: React 19 + Vite + TypeScript, Tailwind CSS, TanStack Query, React Router
- `web/` создан через `npm create vite@latest` (react-ts шаблон)
- Установлены зависимости: react-router-dom, @tanstack/react-query, tailwindcss, @tailwindcss/vite
- Tailwind CSS подключён через Vite plugin в `vite.config.ts`
- Создана структура: `src/api/` (клиент, типы), `src/auth/` (контекст, guard), `src/pages/` (student/parent), `src/components/` (Navbar, PageShell, LevelBadge)
- Vite proxy настроен: `/api` -> `http://localhost:8000`
- Makefile: `web-install`, `web-dev`, `web-build`, `web-lint`
- vision.md обновлён: стек Web, Make-команды, структура репо
- ADR README обновлён
- tasklist-web.md создан
- plan.md обновлён: итерация 4 In Progress с tasklist

## Артефакты

- `web/` — scaffold проекта
- `docs/adr/adr-004-web-stack.md`
- `docs/tasks/tasklist-web.md`
- Обновлены: `Makefile`, `docs/vision.md`, `docs/adr/README.md`, `docs/plan.md`
