# Задача 08: базовое качество и инженерные практики

**Итерация:** iter-2-mvp  
**Статус:** выполнено

## Цель

Единый ruff по монорепо, access-лог с `X-Request-ID` и контекстом клиента без тел и секретов, политика изменения OpenAPI, синхронизация Makefile / README / vision, опционально CI.

## Шаги

1. Корневой `ruff.toml` (target py312, исключения `.venv`, `.agents`, кэши), `ruff format` / `ruff check`.
2. Middleware `AccessLogMiddleware`: заголовок ответа `X-Request-ID`, лог `backend.access` с `channel` / `external_user_id`; путь без query.
3. `docs/vision.md`: изменение контракта API; расширение раздела логирования; команда `make check`.
4. `Makefile` + README: цель `check` (lint + test).
5. Политика тестов — кратко в `tests/conftest.py`.
6. GitHub Actions: ruff + pytest на push/PR.

## Проверка

`make check`; при наличии CI — зелёный workflow.
