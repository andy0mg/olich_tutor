#!/usr/bin/env bash
# Запуск на VPS из каталога приложения (см. deploy/README.md, CI/CD).
set -euo pipefail

DEPLOY_ROOT="${DEPLOY_ROOT:-/opt/olich_tutor}"
cd "$DEPLOY_ROOT"

git fetch origin
branch="$(git rev-parse --abbrev-ref HEAD)"
git reset --hard "origin/${branch}"

.venv/bin/pip install --disable-pip-version-check -r requirements.txt

set -a
# shellcheck disable=SC1091
source .env
set +a

.venv/bin/python -m alembic -c backend/alembic.ini upgrade head

sudo systemctl restart olich-backend olich-bot
