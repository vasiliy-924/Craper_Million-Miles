## Scraper Plan

For `TODO.md:118-144`, build this as a small, testable pipeline, not one big script.

## 1. Target scope
For MVP, scrape `2-3 brands` only.

Recommended start:

- `Toyota` -> `https://carsensor.net/usedcar/bTO/index.html`
- `Honda` -> `https://carsensor.net/usedcar/bHO/index.html`
- `Nissan` -> `https://carsensor.net/usedcar/bNI/index.html`

Keep it configurable so you can limit:

- brands
- max pages per brand
- max cars per run

## 2. Worker structure
Create these files under `backend/worker/scraper/`:

- `client.py`
- `parsers/list_page.py`
- `parsers/detail_page.py`
- `normalizers.py`
- `dictionaries.py`
- `pipeline.py`

Also add:

- `backend/worker/main.py`

## 3. What each file should do

### `client.py`
Purpose: all HTTP fetching logic.

Implement:

- shared `requests.Session()` or `httpx.Client()`
- browser-like headers
- timeout
- retry/backoff
- polite delay between requests

Methods:

- `fetch_html(url: str) -> str`

Settings to use:

- timeout seconds
- retry count
- delay seconds

## 4. `parsers/list_page.py`
Purpose: parse one brand listing page and extract car detail URLs.

Input:

- raw HTML
- base URL

Output:

- `list[str]` of absolute detail URLs

Responsibilities:

- find links like `/usedcar/detail/AU.../index.html`
- ignore lease pages
- deduplicate within page

Also add:

- optional pagination extraction if you want next pages later

## 5. `parsers/detail_page.py`
Purpose: parse one car detail page.

Input:

- raw detail-page HTML
- source URL

Output:

- raw parsed dictionary, for example:

```python
{
    "external_id": "...",
    "source_url": "...",
    "brand_raw": "...",
    "model_raw": "...",
    "price_raw": "...",
    "total_price_raw": "...",
    "year_raw": "...",
    "mileage_raw": "...",
    "fuel_raw": "...",
    "transmission_raw": "...",
    "body_type_raw": "...",
    "dealer_name": "...",
    "main_image_url": "...",
    "image_urls": [...],
    "specs_raw": {...},
}
```

Parse at least:

- title
- brand
- model
- body type if available
- vehicle price
- total price
- year
- mileage
- fuel
- transmission
- dealer
- photos
- spec labels/values

## 6. `dictionaries.py`
Purpose: Japanese-to-English mapping.

Start with dictionaries for:

- brands
- fuel
- transmission
- body type
- common spec labels
- color if practical

Examples:

- `トヨタ -> Toyota`
- `ホンダ -> Honda`
- `日産 -> Nissan`
- `ガソリン -> petrol`
- `ディーゼル -> diesel`
- `ハイブリッド -> hybrid`
- `フロアCVT -> CVT`
- `インパネCVT -> CVT`
- `ハッチバック -> hatchback`
- `ミニバン -> minivan`
- `SUV・クロカン -> SUV`

## 7. `normalizers.py`
Purpose: convert raw Japanese strings into normalized DB-ready fields.

Implement helpers like:

- `extract_external_id(url)`
- `normalize_brand(value)`
- `normalize_model(value)`
- `parse_price_jpy("149.8 万円") -> 1498000`
- `parse_mileage_km("3.5万km") -> 35000`
- `parse_year("2023(R05)") -> 2023`
- `normalize_fuel(value)`
- `normalize_transmission(value)`
- `normalize_body_type(value)`

Output should match your DB schema fields exactly.

## 8. `pipeline.py`
Purpose: orchestrate the scraper flow.

Responsibilities:

1. iterate configured brand URLs
2. fetch list pages
3. extract detail URLs
4. deduplicate across pages
5. fetch each detail page
6. parse raw fields
7. normalize fields
8. save/upsert into DB

Functions:

- `scrape_brand(brand_code: str, max_pages: int) -> list[dict]`
- `scrape_all()`
- `upsert_car(db, normalized_car_data)`

## 9. Stable `external_id`
Use the Carsensor detail URL.

From URLs like:

- `https://carsensor.net/usedcar/detail/AU6888403167/index.html`

extract:

- `AU6888403167`

That should be your stable `external_id`.

## 10. Suggested parsing strategy
Start simple:

### List page
You already confirmed listing pages are server-rendered enough. So first parse:

- detail URLs
- maybe quick summary fields if easy

### Detail page
Treat detail page as source of truth for DB insert.

That avoids inconsistencies from partial list-page data.

## 11. HTTP client rules
In `client.py`, include:

- realistic `User-Agent`
- `Accept-Language: ja,en;q=0.9`
- timeout around `15-30s`
- retries `2-3`
- delay between requests, e.g. `1.0-2.0s`

Do not start with Playwright unless HTML parsing clearly fails.

## 12. Persistence plan
When a normalized car is ready:

- lookup by `external_id`
- if exists: update fields
- if not: insert new row

Update these every scrape:

- `scraped_at`
- `updated_at`

## 13. Recommended implementation order

1. create worker folder structure
2. implement `client.py`
3. implement `extract_external_id()` and core normalizers
4. implement `list_page.py`
5. test extracting detail URLs from one Toyota page
6. implement `detail_page.py`
7. test parsing one known detail page
8. implement dictionaries
9. implement DB upsert in `pipeline.py`
10. wire one-shot run in `backend/worker/main.py`
11. scrape one brand with a very small limit
12. expand to 2-3 brands

## 14. Definition of done for this step
Mark `TODO.md:118-144` done when:

- worker module files exist
- HTTP client supports headers, retry, timeout, delay
- list pages return detail URLs
- detail pages parse required raw fields
- `external_id` is reliably derived from URL
- raw fields are passed into normalization layer
- scraper can process chosen brand pages end-to-end

## 15. Practical MVP target
For the first successful run, aim for:

- 1 brand
- 1 page
- 10-20 cars

After that works, expand to:

- 2-3 brands
- a few pages each

That is the safest path.

If you want, I can next give you the exact interface for each scraper file, including function names, input/output shapes, and what each parser should return.