.PHONY: up down migrate seed build rebuild scrape test test-backend test-frontend test-docker test-backend-docker test-frontend-docker

# One-command startup: start db, run migrations, seed admin, start all services
up:
	cd infra && docker compose up -d db
	@echo "Waiting for PostgreSQL..."
	@sleep 5
	cd infra && docker compose run --rm api alembic upgrade head
	cd infra && docker compose run --rm api python scripts/seed_admin.py
	cd infra && docker compose up -d

# Stop all services
down:
	cd infra && docker compose down

# Run migrations only
migrate:
	cd infra && docker compose run --rm api alembic upgrade head

# Seed admin user only
seed:
	cd infra && docker compose run --rm api python scripts/seed_admin.py

# Build all images
build:
	cd infra && docker compose build

# Rebuild images and start (use after code changes)
rebuild: build up

# Run scraper once (manual trigger)
scrape:
	cd infra && docker compose run --rm worker python -m worker.main

# Run backend tests (requires Docker for testcontainers; activate backend venv first)
test-backend:
	cd backend && python -m pytest tests/ -v

# Run frontend tests
test-frontend:
	cd frontend && npm run test:run

# Run all tests
test: test-backend test-frontend

# Run backend tests via Docker (no venv needed; requires Docker)
test-backend-docker:
	cd infra && docker compose up -d db && sleep 3 && \
	docker compose run --rm api alembic upgrade head && \
	docker compose run --rm -e USE_EXISTING_DB=1 api python -m pytest tests/ -v

# Run frontend tests via Docker (no npm install needed)
test-frontend-docker:
	cd infra && docker compose run --rm frontend-test

# Run all tests via Docker (one command, no local setup)
test-docker: test-backend-docker test-frontend-docker
