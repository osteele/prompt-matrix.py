.PHONY: install
install:
	poetry install

.PHONY: format
format:
	poetry run black .
	poetry run isort .

.PHONY: lint
lint:
	poetry run ruff .
	poetry run black --check .
	poetry run isort --check-only .

.PHONY: typecheck
typecheck:
	poetry run mypy .

.PHONY: test
test:
	poetry run pytest

.PHONY: test-watch
test-watch:
	poetry run pytest-watch

.PHONY: tox
tox:
	poetry run tox

.PHONY: precommit
precommit: format lint typecheck test

.PHONY: publish
publish: format lint typecheck tox
	poetry publish --build --username __token__ --password $PYPI_API_TOKEN
