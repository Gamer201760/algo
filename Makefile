.PHONY: test lint typecheck run pre-commit 

help:
	@echo "Доступные команды:"
	@echo "  make install      - Установить все зависимости"
	@echo "  make test         - Запустить тесты pytest"
	@echo "  make benchmark    - Запустить бенчмарки"
	@echo "  make run          - Запустить приложение"
	@echo "  make lint         - Запустить линтер ruff"
	@echo "  make typecheck    - Запустить проверку типов mypy"
	@echo "  make pre-commit   - Запустить все проверки (lint, typecheck, test)"

install:
	uv sync

run:
	uv run main.py

test:
	uv run pytest -v ./test/ --benchmark-skip

benchmark:
	uv run pytest -v ./test/ --benchmark-only

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

pre-commit: lint typecheck test
