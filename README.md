## Overview

A full-stack application that scrapes used car listings from [Carsensor](https://carsensor.net/), stores them in PostgreSQL, and exposes them via a REST API and a Next.js web app. Data is normalized from Japanese to English. Access is protected by JWT authentication.

## Stack

- **backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, python-jose
- **scraper worker**: Python, httpx/requests, BeautifulSoup, Playwright
- **frontend**: Next.js, TypeScript, Tailwind CSS, TanStack Query, Zustand
- **infra**: Docker Compose

## Local setup

**Prerequisites:** Docker and Docker Compose

1. Clone the repository
2. Run `make up`
3. (Optional) Run `make scrape` to populate the database
4. Open [http://localhost:3000](http://localhost:3000) (frontend) or [http://localhost:8000](http://localhost:8000) (API)

### One-command startup

```bash
make up
```

This will:
1. Start PostgreSQL
2. Run database migrations
3. Seed the admin user (admin / admin123)
4. Start API, worker, and frontend

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API docs**: http://localhost:8000/docs

## Default credentials

- **Username:** `admin`
- **Password:** `admin123`

## API endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | No | Health check |
| POST | `/auth/login` | No | Login (username, password) → JWT |
| GET | `/cars` | Bearer | List cars with filters, sort, pagination |
| GET | `/cars/{id}` | Bearer | Car detail by ID |

### GET /cars query parameters

- `page`, `limit` – pagination
- `brand`, `model` – filter by brand/model
- `min_price`, `max_price` – price range (JPY)
- `min_year`, `max_year` – year range
- `min_mileage`, `max_mileage` – mileage range (km)
- `sort_by`, `sort_order` – sort field and direction (asc/desc)

### Get JWT token

```bash
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## Architecture

```
/backend
  /app
    /api
    /core
    /db
    /models
    /schemas
    /services
  /worker
    /scraper
/frontend
/infra
  docker-compose.yml
```

## Scraping scope

- **Source:** [Carsensor](https://carsensor.net/)
- **Brands:** Toyota, Honda, Nissan
- **Schedule:** Hourly (configurable via worker)
- **Data:** Brand, model, year, mileage, price, fuel, transmission, body type, location, dealer, photos, specs

## Normalization

Japanese values are mapped to English via dictionaries (brands, fuel, transmission, body type, colors, spec labels). Both raw and normalized fields are stored. Unknown values are logged once and kept as-is. Price (`149.8万円`), mileage (`3.5万km`), and year (`2023(R05)年`) are parsed into numeric values.

## Other commands

```bash
make down      # Stop all services
make migrate   # Run migrations only
make seed      # Seed admin user only
make build     # Build all Docker images
make rebuild   # Rebuild images and start (use after code changes)
make scrape    # Run scraper once (manual trigger)
make test               # Run all tests (backend + frontend, needs venv + npm)
make test-backend       # Run backend tests (needs venv)
make test-frontend      # Run frontend tests (needs npm)
make test-docker        # Run ALL tests via Docker (one command, no local setup)
make test-backend-docker   # Run backend tests via Docker
make test-frontend-docker  # Run frontend tests via Docker
```

## Testing (Docker one-liner)

No Python venv or npm install needed. Just run:

```bash
make test-docker
```

This runs backend and frontend tests inside Docker. Requires Docker Desktop to be running.

- `make test-backend-docker` – backend tests only
- `make test-frontend-docker` – frontend tests only

## Manual verification

After `make up`:

1. **Services start** – Frontend at http://localhost:3000, API at http://localhost:8000
2. **Scraper fills DB** – Run `make scrape` to import cars from Carsensor
3. **Login** – Go to `/login`, sign in with `admin` / `admin123`
4. **Cars list** – Browse `/cars`, use filters and pagination
5. **Car detail** – Click a car to view `/cars/[id]` with full specs

## Known limitations

- Scrapes only Toyota, Honda, Nissan
- English-only UI
- No admin panel
- HTML/BeautifulSoup first; Playwright used only when necessary

## Author

**Василий Петров** – [GitHub](https://github.com/vasiliy-924)
