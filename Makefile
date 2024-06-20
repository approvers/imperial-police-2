ifneq (,$(wildcard ./.example.env))
	include .example.env
	export
else ifneq (,$(wildcard ./.local.env))
	include .local.env
	export
endif

.PHONY: build
build:
	docker compose build

.PHONY: up
up:
	docker compose up -d --build
	$(MAKE) logs

.PHONY: down
down:
	docker compose down

.PHONY: logs
logs:
	docker compose logs -f

.PHONY: shell
shell:
	docker compose run --rm python bash

.PHONY: flake8
flake8:
	docker compose run --rm python bash -c "python run_command.py rye run flake8 ./"

.PHONY: mypy
mypy:
	docker compose run --rm python bash -c "python run_command.py rye run mypy ./"

.PHONY: black
black:
	docker compose run --rm python bash -c "python run_command.py rye run black ./"

.PHONY: black_check
black_check:
	docker compose run --rm python bash -c "python run_command.py rye run black ./ --check"

.PHONY: pytest_html
pytest_html:
	docker compose run --rm python bash -c "python run_command.py rye run pytest -v ./test/ --cov=./src/ --cov-report=html"

.PHONY: pytest_xml
pytest_xml:
	docker compose run --rm python bash -c "python run_command.py rye run pytest -v ./test/ --cov=./src/ --cov-report=xml"

.PHONY: pytest_ci
pytest_ci:
	docker compose run --rm python bash -c "python run_command.py rye run pytest -v ./test/ --cov --junitxml=pytest.xml --cov-report=term-missing:skip-covered | tee pytest-coverage.txt"
