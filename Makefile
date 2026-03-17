.PHONY: up down migrate seed build rebuild scrape

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
