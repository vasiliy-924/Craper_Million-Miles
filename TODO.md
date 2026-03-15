Locked scope:

- scrape `2-3 brands`
- optimize for `Docker Compose locally first`
- scraper strategy: `HTML + BeautifulSoup first`, `Playwright` only if needed
- priority: `stability and clean architecture`

Since I’m in Ask mode, I can’t implement it directly from here, but I can give you a build-ready TODO plan. `GET /cars/{id}` is the right call, and we’ll keep the whole app English-only.

## Detailed TODO Plan

### 1. Project bootstrap
- Create monorepo structure:
  - `backend/` ✅
  - `frontend/` ✅
  - `infra/` ✅
- Add root `README.md` with:
  - stack
  - run instructions
  - architecture
  - assumptions and tradeoffs
- Pick scraped brands for MVP:
  - example: `Toyota`, `Honda`, `Nissan`

### 2. Backend foundation
- Initialize `FastAPI` app with modular structure:
  - `app/api` ✅
  - `app/core` ✅ 
  - `app/db` ✅
  - `app/models ✅`
  - `app/schemas` ✅
  - `app/services` ✅
- Add config management with environment variables:
  - DB URL ✅
  - JWT secret ✅
  - token lifetime ✅
  - scraper limits ✅
- Add health endpoint for local verification:
  - `GET /health`  ✅

### 3. Database design
- Set up `PostgreSQL` ✅
- Configure `SQLAlchemy` and `Alembic` ✅
- Create `users` table: ✅
  - `id`
  - `username`
  - `password_hash`
  - `created_at`
- Create `cars` table: ✅
  - `id`
  - `external_id`
  - `source_url`
  - `brand_raw`
  - `brand_normalized`
  - `model_raw`
  - `model_normalized`
  - `year`
  - `mileage_km`
  - `price_jpy`
  - `total_price_jpy`
  - `location_raw`
  - `location_normalized`
  - `fuel_raw`
  - `fuel_normalized`
  - `transmission_raw`
  - `transmission_normalized`
  - `body_type_raw`
  - `body_type_normalized`
  - `color_raw`
  - `dealer_name`
  - `main_image_url`
  - `image_urls`
  - `specs`
  - `scraped_at`
  - `updated_at`
- Add indexes for: ✅
  - `external_id`
  - `brand_normalized`
  - `model_normalized`
  - `price_jpy`
  - `year`
  - `mileage_km`

### 4. Auth ✅
- Seed default user:
  - username: `admin`
  - password: `admin123`
- Implement password hashing
- Implement JWT creation/validation
- Add endpoint:
  - `POST /auth/login`
- Protect car endpoints with bearer token

### 5. Car API ✅
- Implement `GET /cars` ✅
- Support query params: ✅
  - `page`
  - `limit`
  - `brand`
  - `model`
  - `min_price`
  - `max_price`
  - `min_year`
  - `max_year`
  - `min_mileage`
  - `max_mileage`
  - `sort_by`
  - `sort_order`
- Response should include: ✅
  - `items`
  - `total`
  - `page`
  - `limit`
  - `pages`
- Implement `GET /cars/{id}` ✅
- Return full normalized and raw data on detail page

### 6. Scraper architecture
- Create worker module structure:
  - `scraper/client.py`
  - `scraper/parsers/list_page.py`
  - `scraper/parsers/detail_page.py`
  - `scraper/normalizers.py`
  - `scraper/dictionaries.py`
  - `scraper/pipeline.py`
- Add HTTP client with:
  - browser-like headers
  - retry/backoff
  - timeout
  - throttling
- Implement list-page scraping:
  - fetch listing pages for chosen brands
  - extract detail URLs
  - deduplicate links
- Implement detail-page scraping:
  - parse title
  - parse price
  - parse year
  - parse mileage
  - parse fuel/transmission/body type
  - parse dealer name
  - parse photos
  - parse specs table
- Derive stable `external_id` from Carsensor URL

### 7. Translation and normalization
- Build English-only normalization dictionaries for Japanese values:
  - brands
  - fuel types
  - body types
  - transmissions
  - common spec labels
  - prefectures/locations if useful
- Implement converters:
  - `149.8万円 -> 1498000`
  - `3.5万km -> 35000`
  - `2023(R05)年 -> 2023`
- Keep both:
  - raw source fields
  - normalized English fields
- Log unknown Japanese labels so they can be added later

### 8. Persistence pipeline
- Upsert by `external_id`
- Update changed fields on re-scrape
- Keep `scraped_at` / `updated_at`
- Handle partial parse failures without stopping the whole run
- Optionally mark stale cars if no longer seen

### 9. Scheduling
- Add hourly run strategy
- For local Docker MVP, simplest options:
  - worker loop with `sleep 3600`
  - or cron inside worker container
- Also add manual command:
  - one-shot scrape for development/demo

### 10. Frontend foundation
- Initialize `Next.js` with `TypeScript`
- Add `Tailwind CSS`
- Add data fetching with `TanStack Query`
- Add auth state management
- Decide token storage:
  - simplest MVP: `localStorage`
  - cleaner option: cookie-based auth proxy
- For the test, `localStorage` is acceptable if documented

### 11. Frontend pages
- `/login`
  - username/password form
  - stores JWT
  - redirects to cars list
- `/cars`
  - responsive grid/list
  - filters
  - sorting
  - pagination
  - loading and empty states
- `/cars/[id]`
  - gallery
  - summary card
  - specs section
  - source link to Carsensor
- Add route protection for authenticated pages

### 12. UI details
- English-only labels everywhere
- Mobile-first responsive layout
- Car card should show:
  - image
  - brand/model
  - year
  - mileage
  - price
  - location
- Detail page should emphasize:
  - main photo
  - key specs
  - dealer
  - all parsed attributes
- Add graceful fallbacks for:
  - missing image
  - missing price
  - unknown spec values

### 13. Docker and local run
- Add `docker-compose.yml` for:
  - `db`
  - `backend`
  - `worker`
  - `frontend`
- Add env files:
  - backend env
  - frontend env
- Ensure one-command startup
- Make sure DB migrations run cleanly in local setup

### 14. Testing and verification
- Backend:
  - login test
  - cars list filter test
  - car detail test
  - normalization unit tests
- Scraper:
  - parser tests on saved HTML fixtures
  - currency/mileage/year normalization tests
- Frontend:
  - smoke test login
  - smoke test list rendering
  - smoke test detail page
- Manual verification:
  - scrape command fills DB
  - login works with `admin/admin123`
  - filters and pagination work

### 15. Submission polish
- README sections:
  - project overview
  - stack
  - architecture
  - scraping scope
  - normalization approach
  - local setup
  - default credentials
  - API endpoints
  - known limitations
- Include screenshots or GIF if time allows
- Deploy after local Docker is stable

## Recommended build order
1. Backend skeleton + DB + auth
2. `GET /cars` and `GET /cars/{id}`
3. Scraper for one brand
4. Normalization dictionaries
5. Upsert pipeline
6. Expand to 2-3 brands
7. Frontend login
8. Frontend list page
9. Frontend detail page
10. Docker Compose
11. README and final polish

## Scope guardrails
To keep this strong and finishable in 2 days:

- do not scrape the whole marketplace
- do not over-engineer queueing
- do not build admin panels
- do not add multilingual UI
- do not spend too much time on fancy design before scraper/data/API are stable

## Suggested MVP definition
The MVP is done when:

- scraper imports cars from 2-3 brands
- data is normalized into English
- auth works with JWT
- `GET /cars` supports filters, sorting, pagination
- `GET /cars/{id}` returns full detail
- frontend has login, list, and detail pages
- project runs with Docker Compose
- README is clear enough for reviewer to launch in minutes

If you want, next I can turn this into a very concrete file-by-file implementation checklist with exact folders, modules, models, and endpoint contracts.