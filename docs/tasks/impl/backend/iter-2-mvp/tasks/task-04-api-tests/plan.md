# Задача 04: базовые API-тесты — план

**Итерация:** iter-2-mvp  
**Tasklist:** [docs/tasks/tasklist-backend.md](../../../../../../tasks/tasklist-backend.md)

## Решения

| Решение | Детали |
|--------|--------|
| Вариант A (DoD) | Минимальные маршруты `/api/v1/*` с in-memory хранилищем без LLM; задача 05 заменит оркестрацию, контракт сохраняется. |
| Тесты | `httpx.AsyncClient` + `ASGITransport`, изолированный `InMemoryApiStore` через `dependency_overrides`. |
| Заголовки | `Depends(get_client_context)` — `X-Channel` (`Literal`), `X-External-User-Id` (непустой после trim). |

## Файлы

- `tests/conftest.py`, `tests/api/test_v1_conversations.py`, `tests/api/test_v1_knowledge_snapshots.py`
- `pytest.ini` — `asyncio_mode = auto`
- `backend/api/deps.py`, `backend/api/routers/v1/`, `backend/schemas/api_v1.py`, `backend/services/memory_store.py`

## Прогон

```bash
make test
# или: .venv/Scripts/python.exe -m pytest
```
