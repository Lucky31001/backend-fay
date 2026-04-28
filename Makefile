DOCKER ?= docker compose

ifeq ($(OS),Windows_NT)
    PY ?= python3
endif

PIP ?= $(PY) -m pip
MANAGE_PY := FAYProject/manage.py
DJANGO := $(PY) $(MANAGE_PY)

DJANGO_SUPERUSER_USERNAME ?= test
DJANGO_SUPERUSER_EMAIL ?= test@test.test
DJANGO_SUPERUSER_PASSWORD ?= Azerty123!

export DJANGO_SUPERUSER_USERNAME
export DJANGO_SUPERUSER_EMAIL
export DJANGO_SUPERUSER_PASSWORD

.PHONY: install run wait-db migrate migration down logs test admin prettier

install:
	$(PIP) install -r requirements.txt

wait-db:
	$(PY) -c "import time; time.sleep(5)"

run:
	$(DOCKER) up -d
	@$(MAKE) wait-db
	$(DJANGO) migrate
	$(DJANGO) runserver 0.0.0.0:8000

admin:
	$(DJANGO) createsuperuser --noinput

migrate:
	@$(MAKE) wait-db
	$(DJANGO) migrate

migration:
	$(DJANGO) makemigrations
	$(DJANGO) migrate

down:
	$(DOCKER) down -v --remove-orphans

test:
	$(DJANGO) test

prettier:
	$(PY) -m black .
	$(PY) -m isort .
	$(PY) -m ruff check . --fix