# Задача 07: рефакторинг бота под backend API — план

## Цель

Бот — тонкий клиент: `httpx` + заголовки `X-Channel: telegram`, `X-External-User-Id` (Telegram user id). Сценарий (A): `POST /api/v1/conversations`, `POST .../messages`. Без импорта пакета `backend` из процесса бота.

## Решения

- Модуль `bot/backend_client.py`: парсинг JSON ответов по полям OpenAPI.
- Память `conversation_id` по `user_id` в closure роутера; `/start` создаёт новый диалог; при `404` на сообщение — новый диалог и одна повторная отправка.
- Корневой `config.Settings`: `BACKEND_BASE_URL`, `OPENROUTER_*` не обязательны для бота.
- `main.py`: `httpx.AsyncClient` с таймаутом 120 с, `async with` вокруг polling.

## Сценарий (B)

Отдельный UX в боте для knowledge-snapshots не вводился (в боте ранее не было); доступен через API.

## Документация

`README.md`, `docs/vision.md`, `.env.example` — два процесса и ключ LLM на стороне backend.
