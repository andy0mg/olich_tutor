# Задача 04: базовые API-тесты — summary

**Статус:** выполнено

## Сделано

- Зависимости: `httpx`, `pytest`, `pytest-asyncio` в [requirements.txt](../../../../../../../requirements.txt).
- Инфраструктура: [pytest.ini](../../../../../../../pytest.ini), [tests/conftest.py](../../../../../../../tests/conftest.py) с фикстурой `client` и переопределением `get_memory_store`.
- Заглушки API v1: in-memory [backend/services/memory_store.py](../../../../../../../backend/services/memory_store.py), Pydantic-схемы [backend/schemas/api_v1.py](../../../../../../../backend/schemas/api_v1.py), роутеры [backend/api/routers/v1/](../../../../../../../backend/api/routers/v1/), зависимость [backend/api/deps.py](../../../../../../../backend/api/deps.py).
- Тесты: сценарий A (создание диалога, сообщение, GET, 404, 400, невалидный UUID, пустой content, отсутствие заголовков); сценарий B (201 snapshot, 422 без level / пустой topic).
- [Makefile](../../../../../../../Makefile): цель `test`; [README.md](../../../../../../../README.md): строка про `make test`.

## Проверка

- `make test` — 11 тестов (интеграционные async; см. `pytest.ini` `asyncio_mode = auto`), OK.
- `ruff check backend tests` — OK.
