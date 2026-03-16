# backend/worker/main.py
"""
Run the scraper: from backend/ with venv activated:
    python -m worker.main
"""
import sys
from pathlib import Path

# Add backend to path so app can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal  # noqa: E402
from worker.scraper.pipeline import scrape_all  # noqa: E402


def main():
    db = SessionLocal()
    try:
        results, summary = scrape_all(
            db, brands=["TO"], max_pages=1, max_cars=10
        )
        print(f"Scraped {len(results)} cars")
        for r in results:
            print(f"  - {r['external_id']} (id={r['id']})")
        print("\nRun summary:")
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


if __name__ == "__main__":
    main()
