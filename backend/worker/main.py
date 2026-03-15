# backend/worker/main.py
"""
Run the scraper: from backend/ with venv activated:
    python -m worker.main
"""
import sys
from pathlib import Path

# Add backend to path so app can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import SessionLocal
from worker.scraper.pipeline import scrape_all


def main():
    db = SessionLocal()
    try:
        # MVP: 1 brand, 1 page, max 10 cars
        results = scrape_all(db, brands=["TO"], max_pages=1, max_cars=10)
        print(f"Scraped {len(results)} cars")
        for r in results:
            print(f"  - {r['external_id']} (id={r['id']})")
    finally:
        db.close()


if __name__ == "__main__":
    main()