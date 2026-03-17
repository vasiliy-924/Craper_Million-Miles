# backend/worker/main.py
"""
Run the scraper: from backend/ with venv activated:
    python -m worker.main
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone
import time

# Add backend to path so app can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal  # noqa: E402
from worker.scraper.pipeline import scrape_all  # noqa: E402


def _get_config():
    mode = os.environ.get("WORKER_MODE", "once")
    interval = int(os.environ.get("SCRAPE_INTERVAL_SECONDS", "3600"))
    brands_str = os.environ.get("SCRAPER_BRANDS", "TO")
    brands = [b.strip() for b in brands_str.split(",") if b.strip()]
    max_pages = int(os.environ.get("SCRAPER_MAX_PAGES", "1"))
    max_cars = int(os.environ.get("SCRAPER_MAX_CARS", "20"))
    return mode, interval, brands, max_pages, max_cars


def _run_once(db, brands, max_pages, max_cars):
    results, summary = scrape_all(
        db, brands=brands, max_pages=max_pages, max_cars=max_cars
    )
    return results, summary


def main():
    mode, interval, brands, max_pages, max_cars = _get_config()

    db = SessionLocal()
    try:
        start = datetime.now(timezone.utc)
        print(
            f"[{start.isoformat()}] Worker start | mode={mode} | brands={brands} | max_pages={max_pages} | max_cars={max_cars}"
        )

        results, summary = _run_once(db, brands, max_pages, max_cars)

        print(f"Scraped {len(results)} cars")
        for r in results:
            print(f"  - {r['external_id']} (id={r['id']})")
        print("Run summary:")
        print(f"  processed: {summary['processed']}")
        print(f"  inserted:  {summary['inserted']}")
        print(f"  updated:   {summary['updated']}")
        print(f"  failed:    {summary['failed']}")
        print(f"  skipped:   {summary['skipped']}")
        if summary["failed_urls"]:
            print("  Failed URLs:")
            for url in summary["failed_urls"]:
                print(f"    - {url}")
    finally:
        db.close()

    if mode == "loop":
        print(f"Sleeping {interval} seconds before next run...")
        time.sleep(interval)
        main()


if __name__ == "__main__":
    main()
