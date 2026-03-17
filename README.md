## Stack

- **backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, python-jose
- **scraper worker**: Python, httpx/requests, BeautifulSoup, Playwright
- **frontend**: Next.js, TypeScript, Tailwind CSS, TanStack Query
- **infra**: Docker Compose

## One-command startup

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

## Get JWT token

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
/frontend
/infra
  docker-compose.yml
```