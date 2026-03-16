## Step 8 Plan

This step is about making the scraper safe to run repeatedly without duplicating rows or breaking on one bad listing.

## Goal
After step 8, each scrape run should:

- insert new cars
- update existing cars by `external_id`
- refresh timestamps
- continue if one listing fails
- optionally track stale listings

## 1. Confirm current baseline
You already have part of step 8 in `backend/worker/scraper/pipeline.py`:

- upsert by `external_id`
- update fields on existing row
- set `scraped_at`
- set `updated_at`
- catch exceptions per detail page and continue

So step 8 is partly implemented already.

## 2. What still needs to be made explicit
To fully finish step 8, make sure the persistence rules are intentional and verifiable.

You want these guarantees:

1. same `external_id` never creates duplicate rows
2. changed values are updated on re-scrape
3. `scraped_at` updates every successful scrape
4. `updated_at` reflects latest data update
5. one broken page does not stop the whole batch
6. optional stale handling is either implemented or explicitly deferred

## 3. Strengthen upsert behavior
In `upsert_car()` define the contract clearly:

### For existing row
- look up by `external_id`
- overwrite normalized/raw fields with latest parsed data
- set `scraped_at = now`
- set `updated_at = now`

### For new row
- insert with all fields
- set both timestamps

You already do this, so the next step is mostly validation and maybe small cleanup.

## 4. Decide how to treat missing fields on re-scrape
This is important.

If a later scrape returns partial data, should it overwrite a good existing field with `None`?

You need one policy:

### Safer MVP policy
- always update fields when new value is not `None`
- keep old value if new scrape missed that field

This avoids losing data from flaky parsing.

Example:
- old `dealer_name = "Gulliver"`
- new scrape fails to parse dealer
- do not replace with `None`

If you keep the current “blind overwrite” approach, it is simpler, but more brittle.

For a test task, the safer policy is better.

## 5. Add scrape result counters
Make the pipeline report summary stats per run.

Track:

- `inserted`
- `updated`
- `failed`
- `skipped`
- `processed`

For example:

```python
{
  "processed": 10,
  "inserted": 7,
  "updated": 3,
  "failed": 1
}
```

That makes worker output much more credible.

## 6. Improve error handling
Right now you catch exceptions per detail page and continue. That’s good.

Make it slightly more structured:

- print the URL that failed
- print a short error message
- continue to next listing

Optional:
- return failed URLs in the run summary

Do not let one parse failure crash the whole scrape.

## 7. Add stale-listing strategy decision
The TODO says “optionally mark stale cars if no longer seen”.

For MVP, you have two choices:

### Option A: explicitly defer
Do not implement stale marking yet, but note in README:
- stale detection is planned but not enabled in MVP

### Option B: implement minimal stale flag
Add a simple nullable field later such as:
- `is_active`
- `last_seen_at`

Then:
- every scraped row gets `last_seen_at = now`
- rows not seen for a long time can be treated as stale

This requires DB schema changes, so unless you want another migration right now, I’d defer it.

## 8. Add tests for persistence behavior
This is the main thing missing from the step.

Create tests for:

### upsert inserts new row
- first scrape with `external_id=X`
- result: one row created

### upsert updates existing row
- second scrape with same `external_id`
- changed price/year/etc
- result: still one row, values updated

### no duplicate rows
- same `external_id` multiple times
- row count stays `1`

### partial failure does not stop run
- one mocked detail page raises error
- other pages still get processed

## 9. Suggested implementation order

1. review current `upsert_car()` behavior
2. decide overwrite policy for `None` values
3. add run summary counters
4. improve failure logging
5. add persistence tests
6. run scraper twice on same small batch
7. verify:
   - no duplicates
   - updates happen
   - timestamps change appropriately
8. decide whether stale marking is deferred or implemented

## 10. How to verify step 8 in terminal

### Run scraper twice
From `backend/`:

```bash
python -m worker.main
python -m worker.main
```

### Check duplicate prevention
From project root:

```bash
docker compose -f infra/docker-compose.yml exec db psql -U postgres -d cars_db -c "select external_id, count(*) from cars group by external_id having count(*) > 1;"
```

Expected:
- no rows returned

### Check total row count after rerun
```bash
docker compose -f infra/docker-compose.yml exec db psql -U postgres -d cars_db -c "select count(*) from cars;"
```

If you scrape the same exact set twice, count should stay stable.

### Check timestamps
```bash
docker compose -f infra/docker-compose.yml exec db psql -U postgres -d cars_db -c "select external_id, scraped_at, updated_at from cars order by updated_at desc limit 10;"
```

### Check one known row updates rather than duplicates
```bash
docker compose -f infra/docker-compose.yml exec db psql -U postgres -d cars_db -c "select id, external_id, price_jpy, scraped_at, updated_at from cars where external_id = 'AU6757636162';"
```

## 11. Definition of done for step 8
Mark step 8 done when:

- upsert by `external_id` is verified
- repeated scrapes do not create duplicates
- changed fields update on re-scrape
- `scraped_at` / `updated_at` are maintained
- one broken page does not stop the run
- stale handling is either:
  - intentionally deferred and documented, or
  - minimally implemented

## 12. Practical recommendation
For this test, I would finish step 8 as:

- keep upsert
- add verification/tests
- keep partial-failure handling
- defer stale marking with a note

That’s a clean and realistic MVP choice.

If you want, I can next review your current `pipeline.py` specifically against step 8 and tell you exactly which parts are already done versus what still needs to be added.