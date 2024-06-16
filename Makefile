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
