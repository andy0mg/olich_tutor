.PHONY: install run lint format

VENV_PY := .venv/Scripts/python.exe
UV := uv

install:
	python -m venv .venv
	$(UV) pip install -r requirements.txt --python $(VENV_PY)

run:
	$(VENV_PY) main.py

lint:
	$(VENV_PY) -m ruff check .

format:
	$(VENV_PY) -m ruff format .
