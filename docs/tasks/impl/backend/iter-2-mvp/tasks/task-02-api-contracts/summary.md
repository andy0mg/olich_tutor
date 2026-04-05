# Задача 02: контракты API — summary

**Статус:** выполнено  
**Итерация:** iter-2-mvp

## Что сделано

- Добавлен контракт [backend/openapi.yaml](../../../../../../../backend/openapi.yaml) (OpenAPI 3.0.3): сценарии (A) и (B), схемы `Conversation`, `Message`, `KnowledgeSnapshot`, общие заголовки идентификации, ошибки, теги и `servers`.
- В [docs/data-model.md](../../../../../../data-model.md) добавлен раздел «Соответствие полей HTTP API v1» с таблицей сопоставления сущностей и полей API.
- В [requirements.txt](../../../../../../../requirements.txt) добавлена зависимость `openapi-spec-validator` для проверки спецификации.
- Проверка: `openapi_spec_validator.validate_spec` на загруженном YAML проходит без ошибок.

## Definition of Done (tasklist)

- Оба сценария прослеживаются в OpenAPI; имена и смысл полей согласованы с data-model.
- Ошибки и версия API описаны явно; учтена возможность второго клиента (веб) через тот же контракт.
