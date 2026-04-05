# Задача 05: реализация API и логики — план

**Итерация:** iter-2-mvp  
**Tasklist:** [docs/tasks/tasklist-backend.md](../../../../../../tasks/tasklist-backend.md)

## Решения

| Решение | Детали |
|--------|--------|
| LLM | `backend/llm/client.py` — AsyncOpenAI к OpenRouter; `get_llm_client()` singleton в `backend/llm/deps.py` |
| История | `backend/tutor/prompts.py` + `build_chat_messages` в `chat_messages.py` |
| Ход диалога | `backend/services/conversation_turn.post_message_turn` — store только данные, сеть вне store |
| Ошибка LLM | JSON 500 `internal_error` по OpenAPI |
| Тесты | `FakeLLMClient` в `tests/conftest.py`, отдельный тест с `_BrokenLLM` на 500 |

## Файлы

- `backend/config.py` — OPENROUTER_*, LLM_MODEL
- `backend/llm/client.py`, `backend/llm/deps.py`
- `backend/tutor/prompts.py`, `backend/tutor/chat_messages.py`
- `backend/services/memory_store.py` — `append_user_message`, `append_assistant_reply`, `get_messages`
- `backend/services/conversation_turn.py`
- `backend/api/routers/v1/conversations.py`
- `tests/conftest.py`, `tests/api/test_v1_conversations.py`

## Прогон

```bash
make test
```
