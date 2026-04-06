# Деплой на VPS (olich_tutor)

Минимальная схема: **PostgreSQL в Docker** (только localhost), **backend** и **Telegram-бот** — два процесса под **systemd**, секреты в `.env` на сервере (не в git).

## 1. Подготовка сервера (`vps-prep`)

Пример для Ubuntu LTS:

```bash
sudo apt update && sudo apt install -y git python3-venv python3-pip docker.io docker-compose-plugin ufw
sudo usermod -aG docker "$USER"   # перелогиньтесь, чтобы группа применилась
sudo ufw allow OpenSSH
sudo ufw enable
```

Создайте пользователя для приложения (без root):

```bash
sudo adduser --disabled-password olich
sudo mkdir -p /opt/olich_tutor
sudo chown olich:olich /opt/olich_tutor
```

Дальше работайте под `olich` или клонируйте в `/opt/olich_tutor` и выставьте владельца.

Установите **Python 3.11+** (должен совпадать с требованиями [`requirements.txt`](../requirements.txt) в репозитории). На сервере можно использовать `python3 -m venv` и [`uv`](https://docs.astral.sh/uv/) по желанию.

## 2. Секреты и окружение (`secrets-env`)

1. Скопируйте шаблоны и заполните значения на сервере (файлы **не коммитятся**):

   ```bash
   cp deploy/env.production.example /opt/olich_tutor/.env
   cp deploy/env.postgres.example /opt/olich_tutor/deploy/.env.postgres
   chmod 600 /opt/olich_tutor/.env /opt/olich_tutor/deploy/.env.postgres
   ```

2. В `deploy/.env.postgres` задайте сильный `POSTGRES_PASSWORD`.

3. В корневом `.env` на сервере:
   - `TELEGRAM_TOKEN` — от [@BotFather](https://t.me/BotFather);
   - `DATABASE_URL` — строка для async-подключения к Postgres (см. комментарии в [`env.production.example`](env.production.example));
   - `OPENROUTER_API_KEY`, `LLM_MODEL` — для процесса backend;
   - `BACKEND_BASE_URL=http://127.0.0.1:8000` — если бот и API на одной машине.

Пароль БД в `DATABASE_URL` должен совпадать с `POSTGRES_PASSWORD` в `deploy/.env.postgres`.

## 3. PostgreSQL только на localhost (`postgres-compose`)

Из каталога репозитория на сервере:

```bash
cd /opt/olich_tutor
docker compose -f deploy/docker-compose.postgres.yml --env-file deploy/.env.postgres up -d
```

Порт **5432** проброшен только на `127.0.0.1` (снаружи VPS недоступен). Брандмауэр не открывайте для PostgreSQL.

## 4. Код, venv, миграции (`deploy-app`)

```bash
cd /opt/olich_tutor
git clone <ваш-репозиторий> .   # или git pull
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
# или: make install — при наличии make и uv локально
set -a && source .env && set +a
.venv/bin/python -m alembic -c backend/alembic.ini upgrade head
```

`DATABASE_URL` должен быть доступен в окружении при вызове Alembic (через `source .env` или `Environment` в systemd).

## 5. systemd (`systemd`)

1. Скопируйте unit-файлы и подставьте пользователя/пути:

   ```bash
   sudo cp deploy/systemd/olich-backend.service /etc/systemd/system/
   sudo cp deploy/systemd/olich-bot.service /etc/systemd/system/
   sudo nano /etc/systemd/system/olich-backend.service   # при необходимости: User, Group, WorkingDirectory, ExecStart
   sudo systemctl daemon-reload
   sudo systemctl enable --now olich-backend olich-bot
   ```

2. Проверка:

   ```bash
   sudo systemctl status olich-backend olich-bot
   journalctl -u olich-backend -u olich-bot -f
   ```

Unit-файлы по умолчанию: `WorkingDirectory=/opt/olich_tutor`, один общий [`EnvironmentFile`](../deploy/systemd/olich-backend.service) на корневой `.env` (см. комментарии внутри unit’ов).

## 6. CI/CD (GitHub Actions)

После успешного **CI** (ruff + pytest) при **push** в `main` или `master` может выполняться автодеплой на VPS — см. [`.github/workflows/ci.yml`](../.github/workflows/ci.yml), job `deploy`.

### Включение

1. В GitHub: **Settings → Secrets and variables → Actions → Variables** — создайте переменную **`DEPLOY_TO_VPS`** со значением **`true`**. Пока переменная не задана или не равна `true`, job деплоя **не запускается** (удобно для форков и до настройки сервера).

2. В том же разделе добавьте **Secrets**:
   - **`VPS_HOST`** — IP или hostname VPS;
   - **`VPS_USERNAME`** — пользователь SSH (например `olich`);
   - **`VPS_SSH_KEY`** — **приватный** ключ для входа на VPS (содержимое `~/.ssh/id_ed25519` или отдельного ключа только для Actions; **не** кладите ключ в репозиторий).

3. На VPS в `~/.ssh/authorized_keys` должен быть соответствующий **публичный** ключ.

4. Скрипт на сервере: [`deploy/deploy.sh`](deploy.sh) — `chmod +x deploy/deploy.sh` после первого клонирования или после `git pull`, который добавил файл.

5. **Sudo без пароля** для перезапуска unit’ов (один раз от root):

   ```text
   olich ALL=(ALL) NOPASSWD: /bin/systemctl restart olich-backend, /bin/systemctl restart olich-bot
   ```

   Файл, например `/etc/sudoers.d/olich-olich-tutor`, создайте через `sudo visudo -f /etc/sudoers.d/olich-olich-tutor`.

6. Репозиторий на VPS: `git pull` должен работать. Для **приватного** репозитория добавьте на сервер [Deploy key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys#deploy-keys) (read-only) в `~/.ssh` и `git remote` на SSH-URL GitHub.

Секреты приложения (**`TELEGRAM_TOKEN`**, **`DATABASE_URL`**, **`OPENROUTER_API_KEY`**) по-прежнему только в **`/opt/olich_tutor/.env` на VPS** — workflow их не копирует.

Порт SSH в workflow по умолчанию **22**. Другой порт — измените поле `port` в job `deploy` в [`ci.yml`](../.github/workflows/ci.yml).

## 7. Обновление после `git pull` (вручную)

```bash
cd /opt/olich_tutor
git pull
.venv/bin/pip install -r requirements.txt
set -a && source .env && set +a
.venv/bin/python -m alembic -c backend/alembic.ini upgrade head
sudo systemctl restart olich-backend olich-bot
```

Либо выполните **`bash /opt/olich_tutor/deploy/deploy.sh`** — те же шаги, что и в CI.

## 8. Опционально позже (`optional-later`)

- **Dockerfile** для API и бота + общий `docker compose` — см. [optional-compose.md](optional-compose.md).
- **Webhook Telegram** + **Nginx + TLS** — когда понадобится публичный HTTPS; сейчас достаточно **polling** ([`docs/vision.md`](../docs/vision.md)).

## Порты и безопасность

| Сервис    | Доступ снаружи VPS |
|-----------|--------------------|
| SSH       | по политике ufw    |
| Backend   | не обязателен (127.0.0.1:8000) |
| Postgres  | нет (только 127.0.0.1) |

При появлении веб-клиента или webhook откройте 80/443 и настройте reverse proxy отдельно.
