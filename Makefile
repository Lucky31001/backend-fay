DOCKER := docker compose
PY := python
MANAGE_PY := FAYProject/manage.py

.PHONY: run start-db wait-db migrate start-app down logs

# High-level target: start DB, wait, migrate, start web (background)
run: start-db migrate start-app
	@echo "Application started (logs: $(LOG))"

start-db:
	@echo "Starting postgres..."
	$(DOCKER) up -d

admin:
	@echo "Creating admin user..."
	$(PY) $(MANAGE_PY) createsuperuser

migrate:
	@echo "Waiting for database to be ready..."
	sleep 10
	@echo "Applying migrations..."
	$(PY) $(MANAGE_PY) migrate

migration:
	@echo "Creating new migration..."
	$(PY) $(MANAGE_PY) makemigrations
	$(PY) $(MANAGE_PY) migrate

start-app:
	@echo "Starting Django dev server (background)..."
	@$(PY) FAYProject/manage.py runserver

down:
	$(DOCKER) down -v --remove-orphans
