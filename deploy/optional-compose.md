# Опционально: Docker для API и бота

Сейчас в репозитории **нет Dockerfile** для приложения. Минимальный прод-деплой описан в [README.md](README.md) (venv + systemd).

Когда понадобится воспроизводимый образ:

1. Добавить `Dockerfile` в корень или `backend/Dockerfile` с установкой зависимостей из `requirements.txt` и точкой входа `python -m backend` или `uvicorn`.
2. Отдельный образ/стадия для бота с `CMD ["python", "main.py"]`.
3. Расширить Compose: сервисы `api`, `bot`, `postgres`, общая сеть, `DATABASE_URL` на `postgres:5432` внутри сети.
4. Секреты передавать через `env_file` или Docker secrets, не копировать `.env` в образ.

Webhook Telegram и Nginx с TLS настраиваются поверх публичного HTTP(S) endpoint — вне scope текущего MVP.
