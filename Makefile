.PHONY: install run run-backend lint format test check db-up db-down db-reset db-migrate db-shell docker-ready

VENV_PY := .venv/Scripts/python.exe
UV := uv

install:
	python -m venv .venv
	$(UV) pip install -r requirements.txt --python $(VENV_PY)

run:
	$(VENV_PY) main.py

run-backend:
	$(VENV_PY) -m backend

lint:
	$(VENV_PY) -m ruff check .

format:
	$(VENV_PY) -m ruff format .

test:
	$(VENV_PY) -m pytest

check: lint test

docker-ready:
	$(VENV_PY) scripts/check_docker.py

db-up: docker-ready
	docker compose up -d --wait

db-down: docker-ready
	docker compose stop

db-reset: docker-ready
	docker compose down -v
	docker compose up -d --wait
	$(VENV_PY) -m alembic -c backend/alembic.ini upgrade head

db-migrate:
	$(VENV_PY) -m alembic -c backend/alembic.ini upgrade head

db-shell: docker-ready
	docker compose exec postgres psql -U olich -d olich_tutor
