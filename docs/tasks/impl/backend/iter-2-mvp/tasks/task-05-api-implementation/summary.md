# Задача 05: реализация API и логики — summary

## Сделано

- Реализован stateless `LLMClient` и DI `get_llm_client`; конфиг backend расширен переменными OpenRouter (как в корневом `.env.example`).
- Сценарий (A): POST `/messages` вызывает `post_message_turn` — добавление user-сообщения, сбор `[system, …]` для `chat`, ответ LLM, запись assistant-сообщения; заглушка `[stub]` удалена.
- Сценарий (B): без изменений — снимки знаний по-прежнему только in-memory store.
- Тесты: подмена LLM фиксированным ответом; тест на 500 при исключении из `chat`.
- Системный промпт продублирован в `backend/tutor/prompts.py` (согласован с `tutor/session.py`).

## Проверка

- `make test` — все тесты зелёные.
