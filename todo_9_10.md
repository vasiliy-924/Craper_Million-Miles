## Next Plan

You’re at two separate next blocks:

- `### 9. Scheduling`
- `### 10. Frontend foundation`

Do them in that order.

## Step 9: Scheduling

### Goal
Make the scraper runnable in two ways:

- one-shot run for manual/dev use
- automatic hourly run for local Docker MVP

## Recommended MVP approach
Use the simplest setup:

- `one-shot`: `python -m worker.main`
- `scheduled`: loop inside a worker container with `sleep 3600`

Do **not** use cron unless you really want it. A simple loop is easier for this test.

## What to add

### 1. Keep manual command
You already have this basically:

- `python -m worker.main`

That satisfies:
- `Also add manual command`
- useful for development/demo

### 2. Add worker mode switch
In `backend/worker/main.py`, support two modes:

- `once`
- `loop`

Behavior:
- `once`: scrape once and exit
- `loop`: run scrape, sleep 3600, repeat

You can drive this with env vars like:

- `WORKER_MODE=once|loop`
- `SCRAPE_INTERVAL_SECONDS=3600`
- `SCRAPER_BRANDS=TO,HO,NI`
- `SCRAPER_MAX_PAGES=1`
- `SCRAPER_MAX_CARS=20`

### 3. Add worker container
In `infra/docker-compose.yml`, add a `worker` service.

It should:
- build from `backend/`
- use the same env as backend
- depend on `db`
- run the worker entrypoint instead of API

Example idea:
- `api` runs `uvicorn`
- `worker` runs `python -m worker.main`

### 4. Print clear worker logs
Each run should log:

- start time
- brands/pages/cars config
- summary from pipeline
- sleep duration before next run

That makes the worker easy to demo.

## Definition of done for step 9
Mark scheduling done when:

- one-shot worker command works
- worker can run in loop mode
- Docker has a dedicated worker service
- interval is configurable
- hourly strategy exists for local MVP

---

## Step 10: Frontend foundation

### Goal
Bootstrap the frontend stack only, not full pages yet.

## Recommended stack
Use:

- `Next.js`
- `TypeScript`
- `Tailwind CSS`
- `TanStack Query`

For auth state, keep it simple:
- token in `localStorage`

That matches your MVP plan.

## What to add

### 1. Initialize frontend app
Create a Next app with TypeScript.

If using App Router, that’s fine.

### 2. Add Tailwind
Set up:
- Tailwind
- global styles
- basic layout shell

### 3. Add TanStack Query
Create:
- `QueryClient`
- provider wrapper
- app-level provider

### 4. Add API configuration
Create a small API layer:

- base API URL from env
- helper for authenticated requests
- login request helper
- cars list fetch helper
- car detail fetch helper

### 5. Add auth state management
Keep it minimal.

Suggested pieces:
- `getToken()`
- `setToken()`
- `clearToken()`
- `isAuthenticated()`

You can later wrap this in context or Zustand, but you do not need that yet.

### 6. Add frontend env
Add something like:

- `NEXT_PUBLIC_API_URL=http://localhost:8000`

### 7. Add base app structure
Suggested early folders:

- `src/app` or `app`
- `src/components`
- `src/lib/api`
- `src/lib/auth`
- `src/providers`

## Recommended implementation order

1. finish step 9 worker modes
2. add `worker` service to Docker Compose
3. initialize `frontend/` with Next + TS
4. add Tailwind
5. add TanStack Query provider
6. add API client helpers
7. add token helpers in `localStorage`
8. verify frontend boots locally

## What not to do yet
Leave these for the next frontend steps:

- login page UI
- cars list page
- detail page
- route protection UI

Those belong after the foundation is in place.

## Very practical order
If you want the smoothest path:

1. `Scheduling` first
2. verify worker can run once and in loop
3. then bootstrap `frontend`
4. then move to `/login`, `/cars`, `/cars/[id]`

If you want, I can next give you:
- an exact plan just for `Step 9`
or
- an exact file/folder plan just for `Step 10 frontend foundation`