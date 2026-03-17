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
```

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