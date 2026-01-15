DOCKER := docker compose
PY := python
MANAGE_PY := .\FAYProject\manage.py

.PHONY: run start-db wait-db migrate start-app down logs

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# High-level target: start DB, wait, migrate, start web (background)
run: start-db migrate start-app
	@echo "Application started (logs: $(LOG))"

start-db:
	@echo "Starting postgres..."
	$(DOCKER) up -d

start-app:
	@echo "Starting Django dev server (listening on 0.0.0.0:8000)..."
	@$(PY) $(MANAGE_PY) runserver 0.0.0.0:8000

admin:
	@echo "Creating admin user..."
	DJANGO_SUPERUSER_USERNAME=test \
	DJANGO_SUPERUSER_EMAIL=test@test.test \
	DJANGO_SUPERUSER_PASSWORD=test \
	$(PY) $(MANAGE_PY) createsuperuser --noinput

migrate:
	@echo "Waiting for database to be ready..."
	timeout /t 10 || true
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
