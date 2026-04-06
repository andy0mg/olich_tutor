# Задача 01: Стек и каркас веб-клиента — план

**Итерация:** iter-4-web-client
**Tasklist:** [docs/tasks/tasklist-web.md](../../../../../tasklist-web.md)

## Цель

Зафиксировать веб-стек (ADR-004), создать каркас `web/`, настроить Tailwind CSS, добавить Makefile-команды, обновить vision.md.

## Состав работ

1. ADR-004: React 19 + Vite + TypeScript + Tailwind + TanStack Query + React Router
2. Scaffold `web/` через `npm create vite` (react-ts)
3. Установка runtime-зависимостей
4. Настройка Tailwind CSS через `@tailwindcss/vite` plugin
5. Структура каталогов: `src/api/`, `src/auth/`, `src/pages/`, `src/components/`
6. Заглушки основных страниц и layout'ов
7. Makefile: `web-install`, `web-dev`, `web-build`, `web-lint`
8. Обновление docs: vision.md (стек, Make-команды, структура репо), ADR README
9. Создание tasklist-web.md
