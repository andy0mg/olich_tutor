# Как получить токены для бота

Краткие шаги без примеров секретов. Ключи храните только в `.env`, не вставляйте их в чаты и в репозиторий.

## Telegram: бот и `TELEGRAM_TOKEN`

1. Откройте Telegram и начните диалог с официальным ботом [**@BotFather**](https://t.me/botfather).
2. Отправьте команду `/newbot`.
3. Задайте отображаемое имя бота и **уникальный** username (заканчивается на `bot`).
4. BotFather пришлёт **токен доступа к HTTP API** — это значение для переменной `TELEGRAM_TOKEN` в `.env`.

Официально о создании бота и токене: раздел **«Creating a new bot»** в [руководстве по возможностям ботов](https://core.telegram.org/bots/features#creating-a-new-bot); общий путь «от BotFather к первому запуску» — [туториал](https://core.telegram.org/bots/tutorial) (блок про получение токена). Справочник по методам API: [Bot API](https://core.telegram.org/bots/api).

При утечке токена отзовите его в BotFather (`/revoke`) и создайте новый.

## OpenRouter: аккаунт и `OPENROUTER_API_KEY`

1. Зайдите на [**openrouter.ai**](https://openrouter.ai) и зарегистрируйтесь или войдите (способ входа зависит от текущего интерфейса сайта).
2. Откройте страницу [**Keys**](https://openrouter.ai/keys) (создание и управление API-ключами).
3. Создайте новый ключ, при необходимости задайте имя и лимит расходов.
4. Скопируйте ключ **один раз** при показе и сохраните в `OPENROUTER_API_KEY` в `.env`.

Официально про использование ключа (Bearer и т.д.): [Authentication](https://openrouter.ai/docs/api/reference/authentication). Быстрый старт по API: [Quickstart](https://openrouter.ai/docs/quickstart).

Если ключ мог попасть в чужие руки — удалите его в настройках и выпустите новый: [настройки ключей](https://openrouter.ai/settings/keys).

## Куда подставить в проекте

См. корневой **`.env.example`**: `TELEGRAM_TOKEN`, `OPENROUTER_API_KEY`, при необходимости `OPENROUTER_BASE_URL` и `LLM_MODEL`.
