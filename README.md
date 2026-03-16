



## Stack:
    backend: FastAPI, SQLAlchemy, Alembic, PostgreSQL, python-jose
    scraper worker: Python, httpx/requests, BeautifulSoup, Playwright
    frontend: Next.js, TypeScript, Taiwind CSS, TanStack Query
    infra: Docker Compose

## Architecture
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
/docker-compose.yml
/README.md



Get JWT token
```bash
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```


