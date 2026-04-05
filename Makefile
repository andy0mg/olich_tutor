.PHONY: install run run-backend lint format test check

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
