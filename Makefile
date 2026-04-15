DOCKER := docker compose
PY := python
MANAGE_PY := FAYProject/manage.py

.PHONY: run start-db wait-db migrate start-app down logs

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# High-level target: start DB, wait, migrate, start web (background)
run:
	$(DOCKER) up -d
	$(PY) $(MANAGE_PY) migrate
	@$(PY) $(MANAGE_PY) runserver 0.0.0.0:8000
	@echo "Application started (logs: $(LOG))"

admin:
	@echo "Creating admin user..."
	DJANGO_SUPERUSER_USERNAME=test \
	DJANGO_SUPERUSER_EMAIL=test@test.test \
	DJANGO_SUPERUSER_PASSWORD=test \
	$(PY) $(MANAGE_PY) createsuperuser --noinput

migrate:
	@echo "Waiting for database to be ready..."
	@sleep 5
	@echo "Applying migrations..."
	$(PY) $(MANAGE_PY) migrate

migration:
	@echo "Creating new migration..."
	$(PY) $(MANAGE_PY) makemigrations
	$(PY) $(MANAGE_PY) migrate

down:
	$(DOCKER) down -v --remove-orphans

test:
	@echo "Running tests..."
	$(PY) $(MANAGE_PY) test

prettier:
	black .
	isort .
	ruff check . --fix
