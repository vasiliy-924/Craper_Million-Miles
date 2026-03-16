## Step 7 Plan

This step is about making scraped data usable in English, not just collecting raw Japanese strings.

## Goal
After step 7, each car should keep:

- original raw Japanese values
- normalized English/internal values

Example:

- `fuel_raw = "ガソリン"`
- `fuel_normalized = "petrol"`

## 1. Expand `dictionaries.py`
Your current `backend/worker/scraper/dictionaries.py` already has a start. Now make it a fuller normalization dictionary file.

Add/expand dictionaries for:

- brands
- fuel types
- body types
- transmissions
- common spec labels
- prefectures / locations
- optionally colors

### Brands
You already have:
- `トヨタ -> Toyota`
- `ホンダ -> Honda`
- `日産 -> Nissan`

Add other common ones if your chosen brands/pages expose them in related fields.

### Fuel
Expand beyond the basics:

- `ガソリン -> petrol`
- `ディーゼル -> diesel`
- `ハイブリッド -> hybrid`
- `電気 -> electric`
- `軽油 -> diesel`
- `レギュラー -> petrol`

### Body types
Normalize Carsensor variations:

- `ハッチバック -> hatchback`
- `ミニバン -> minivan`
- `SUV・クロカン -> SUV`
- `クロカン・ＳＵＶ -> SUV`
- `セダン -> sedan`
- `クーペ -> coupe`
- `コンパクトカー -> compact`
- `軽自動車 -> kei`
- `その他 -> other`

### Transmissions
Map all common display variants to a smaller English/internal set:

- `フロアCVT -> CVT`
- `インパネCVT -> CVT`
- `MTモード付CVT -> CVT`
- `インパネ4AT -> AT`
- `フロア6AT -> AT`
- `フロアMT -> MT`
- `その他AT -> AT`

Important: many values are noisy like `フロアMTモード付CVT`, so exact match may not be enough. You may need pattern-based normalization in `normalizers.py`.

### Spec labels
Map Japanese labels to internal field names:

- `年式(初度登録年)` -> `year`
- `走行距離` -> `mileage_km`
- `本体価格` -> `price_jpy`
- `支払総額` -> `total_price_jpy`
- `ミッション` -> `transmission`
- `エンジン種別` -> `fuel`
- `ボディタイプ` -> `body_type`
- `販売店` or dealer-related labels -> `dealer_name`

### Prefectures / locations
If you want cleaner UI/filtering later, add:

- `北海道 -> Hokkaido`
- `東京都 -> Tokyo`
- `大阪府 -> Osaka`
- `愛知県 -> Aichi`

This is optional but useful.

## 2. Strengthen `normalizers.py`
This is the main work of step 7.

You already have:

- `extract_external_id()`
- `parse_price_jpy()`
- `parse_mileage_km()`
- `parse_year()`
- `normalize_brand()`
- `normalize_fuel()`
- `normalize_transmission()`
- `normalize_body_type()`

Now improve them to handle noisy real-world strings.

## 3. Make normalization pattern-based, not only exact-map based

### Transmission
Current values can look like:

- `フロアCVT`
- `インパネCVT`
- `フロアMTモード付CVT`
- `インパネ4AT`
- `その他AT`

So in `normalize_transmission()`:

- if string contains `CVT` -> `CVT`
- elif contains `AT` -> `AT`
- elif contains `MT` -> `MT`

Dictionary lookup can still happen first.

### Fuel
Similarly:

- if contains `ハイブリッド` -> `hybrid`
- if contains `ガソリン` or `レギュラー` -> `petrol`
- if contains `ディーゼル` or `軽油` -> `diesel`
- if contains `電気` or `EV` -> `electric`

### Body type
Handle display variants and full-width characters:

- `SUV・クロカン`
- `クロカン・ＳＵＶ`

Normalize by checking substrings too.

## 4. Improve numeric converters

### `parse_price_jpy()`
It already handles `149.8万円 -> 1498000`.

Add support for:
- `263万円`
- `45km` should not accidentally parse as price
- possible spaces like `149.8 万円`

### `parse_mileage_km()`
Right now it handles `3.5万km`, which is good.

Also support:
- `12km`
- `300km`
- `1,200km`
- `0.3万km`

So the function should parse both:
- `X万km`
- plain `NNNNkm`

### `parse_year()`
Already okay for:
- `2023(R05)年`

That likely covers the requirement.

## 5. Keep raw + normalized fields
This is already aligned with your DB schema.

Keep examples like:

- `brand_raw` + `brand_normalized`
- `fuel_raw` + `fuel_normalized`
- `transmission_raw` + `transmission_normalized`
- `body_type_raw` + `body_type_normalized`
- `location_raw` + `location_normalized`

Do not overwrite raw fields.

## 6. Add location normalization
You currently have room in DB for:

- `location_raw`
- `location_normalized`

So step 7 should start filling them.

From Carsensor pages you often have:
- prefecture
- city

MVP normalization strategy:
- keep full raw location string
- map prefecture into English if it appears at the start

Examples:
- `北海道函館市` -> raw full string, normalized `Hokkaido`
- `愛知県名古屋市港区` -> normalized `Aichi`

This is enough for now.

## 7. Log unknown values
This is explicitly in the TODO, so add lightweight logging.

You do not need a complex logger for MVP.

Best simple approach:
- whenever a normalizer cannot map a non-empty value cleanly, print a warning like:
  - `Unknown fuel value: ...`
  - `Unknown transmission value: ...`
  - `Unknown body type: ...`
  - `Unknown spec label: ...`

If you want to avoid noisy duplicates, keep a small in-memory `set()` of already-logged unknown values per run.

## 8. Update pipeline normalization output
`normalize_to_db()` in `backend/worker/scraper/pipeline.py` should ensure all normalized fields are filled where possible.

Add/check:

- `location_raw`
- `location_normalized`
- maybe `color_raw` if parser can collect it
- maybe future `specs_translated` later, but not required now

## 9. Suggested implementation order

1. expand dictionaries in `dictionaries.py`
2. improve `normalize_transmission()`
3. improve `normalize_fuel()`
4. improve `normalize_body_type()`
5. improve `parse_mileage_km()` for both `万km` and plain `km`
6. add location normalization
7. add unknown-value logging
8. update `pipeline.normalize_to_db()`
9. run scraper again on 5-10 cars
10. inspect DB/API output

## 10. How to verify step 7
After implementing, check these:

### Normalizer unit-style checks
```bash
python - <<'PY'
from worker.scraper.normalizers import (
    parse_price_jpy, parse_mileage_km, parse_year,
    normalize_fuel, normalize_transmission, normalize_body_type
)

print(parse_price_jpy("149.8万円"))
print(parse_mileage_km("3.5万km"))
print(parse_mileage_km("12km"))
print(parse_year("2023(R05)年"))
print(normalize_fuel("ガソリン"))
print(normalize_transmission("フロアMTモード付CVT"))
print(normalize_body_type("クロカン・ＳＵＶ"))
PY
```

Expected roughly:
- `1498000`
- `35000`
- `12`
- `2023`
- `petrol`
- `CVT`
- `SUV`

### Re-run scraper
```bash
python -m worker.main
```

### Inspect DB
```bash
docker compose -f ../infra/docker-compose.yml exec db psql -U postgres -d cars_db -c "select external_id, fuel_raw, fuel_normalized, transmission_raw, transmission_normalized, body_type_raw, body_type_normalized, location_raw, location_normalized from cars limit 10;"
```

### Check API
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.access_token')

curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8000/cars/1
```

## 11. Definition of done
Mark step 7 done when:

- dictionaries are meaningfully expanded
- `149.8万円 -> 1498000` works
- `3.5万km -> 35000` works
- `2023(R05)年 -> 2023` works
- raw fields are preserved
- normalized English fields are stored
- unknown values are logged for future mapping
- scraped DB rows show English normalized values in the expected columns

If you want, I can next give you a very practical “what to change in each current file” plan specifically for your existing `dictionaries.py`, `normalizers.py`, and `pipeline.py`.