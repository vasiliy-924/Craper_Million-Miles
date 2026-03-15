# backend/worker/scraper/pipeline.py
from datetime import datetime, timezone
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.models.car import Car

from .client import ScraperClient
from .normalizers import (
    extract_external_id,
    normalize_brand,
    normalize_model,
    normalize_fuel,
    normalize_transmission,
    normalize_body_type,
    parse_price_jpy,
    parse_mileage_km,
    parse_year,
)
from .parsers.detail_page import parse_detail_page
from .parsers.list_page import extract_detail_urls

BRAND_URLS = {
    "TO": "https://carsensor.net/usedcar/bTO/index.html",
    "HO": "https://carsensor.net/usedcar/bHO/index.html",
    "NI": "https://carsensor.net/usedcar/bNI/index.html",
}


def get_brand_list_url(brand_code: str, page: int = 1) -> str:
    base = BRAND_URLS.get(brand_code.upper())
    if not base:
        raise ValueError(f"Unknown brand: {brand_code}")
    if page <= 1:
        return base
    return base.replace("/index.html", f"/{page}/index.html")


def normalize_to_db(raw: dict[str, Any]) -> dict[str, Any]:
    """Convert raw parsed dict to DB-ready format."""
    return {
        "external_id": raw.get("external_id") or extract_external_id(raw.get("source_url", "")),
        "source_url": raw.get("source_url", ""),
        "brand_raw": raw.get("brand_raw"),
        "brand_normalized": normalize_brand(raw.get("brand_raw")),
        "model_raw": raw.get("model_raw"),
        "model_normalized": normalize_model(raw.get("model_raw")),
        "year": parse_year(raw.get("year_raw")),
        "mileage_km": parse_mileage_km(raw.get("mileage_raw")),
        "price_jpy": parse_price_jpy(raw.get("price_raw")),
        "total_price_jpy": parse_price_jpy(raw.get("total_price_raw")),
        "fuel_raw": raw.get("fuel_raw"),
        "fuel_normalized": normalize_fuel(raw.get("fuel_raw")),
        "transmission_raw": raw.get("transmission_raw"),
        "transmission_normalized": normalize_transmission(raw.get("transmission_raw")),
        "body_type_raw": raw.get("body_type_raw"),
        "body_type_normalized": normalize_body_type(raw.get("body_type_raw")),
        "dealer_name": raw.get("dealer_name"),
        "main_image_url": raw.get("main_image_url"),
        "image_urls": raw.get("image_urls") or [],
        "specs": raw.get("specs_raw") or {},
    }


def upsert_car(db: Session, data: dict[str, Any]) -> Car:
    """Insert or update car by external_id."""
    now = datetime.now(timezone.utc)
    existing = db.query(Car).filter(Car.external_id == data["external_id"]).first()

    if existing:
        for k, v in data.items():
            setattr(existing, k, v)
        existing.scraped_at = now
        existing.updated_at = now
        db.commit()
        db.refresh(existing)
        return existing

    car = Car(**data, scraped_at=now, updated_at=now)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def scrape_brand(
    client: ScraperClient,
    db: Session,
    brand_code: str,
    max_pages: int = 1,
    max_cars: Optional[int] = None,
) -> list[dict]:
    """Scrape one brand and upsert cars."""
    seen_urls: set[str] = set()
    ordered_urls: list[str] = []
    for page in range(1, max_pages + 1):
        url = get_brand_list_url(brand_code, page)
        html = client.fetch_html(url)
        urls = extract_detail_urls(html, url)
        for detail_url in urls:
            if detail_url in seen_urls:
                continue
            seen_urls.add(detail_url)
            ordered_urls.append(detail_url)
            if max_cars and len(ordered_urls) >= max_cars:
                break
        if max_cars and len(ordered_urls) >= max_cars:
            break

    # Keep first-seen order for reproducible scraping.
    urls_list = ordered_urls
    if max_cars:
        urls_list = urls_list[:max_cars]
    results = []

    for detail_url in urls_list:
        try:
            html = client.fetch_html(detail_url)
            raw = parse_detail_page(html, detail_url)
            raw["external_id"] = raw.get("external_id") or extract_external_id(detail_url)
            if not raw["external_id"]:
                continue
            normalized = normalize_to_db(raw)
            car = upsert_car(db, normalized)
            results.append({"external_id": car.external_id, "id": car.id})
        except Exception as e:
            print(f"Error scraping {detail_url}: {e}")

    return results


def scrape_all(
    db: Session,
    brands: list[str] | None = None,
    max_pages: int = 1,
    max_cars: Optional[int] = 20,
) -> list[dict]:
    """Scrape configured brands."""
    brands = brands or ["TO"]
    client = ScraperClient()
    all_results = []
    for brand in brands:
        all_results.extend(scrape_brand(client, db, brand, max_pages, max_cars))
    return all_results