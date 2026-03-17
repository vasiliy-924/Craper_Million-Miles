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
    normalize_location,
    parse_price_jpy,
    parse_mileage_km,
    parse_year,
)
from .dictionaries import SPEC_LABEL_MAP, SPEC_VALUE_MAP
from .parsers.detail_page import parse_detail_page
from .parsers.list_page import extract_detail_urls


def _translate_specs(specs: dict[str, Any]) -> dict[str, Any]:
    """Translate Japanese spec keys and values to English."""
    if not specs:
        return {}
    result = {}
    for k, v in specs.items():
        key_en = SPEC_LABEL_MAP.get(k, k)
        if isinstance(v, str):
            val_en = SPEC_VALUE_MAP.get(v.strip(), v)
            result[key_en] = val_en
        else:
            result[key_en] = v
    return result


BRAND_URLS = {
    "TO": "https://carsensor.net/usedcar/bTO/index.html",
    "HO": "https://carsensor.net/usedcar/bHO/index.html",
    "NI": "https://carsensor.net/usedcar/bNI/index.html",
}

# processed, inserted, updated, failed, skipped, failed_urls
RunSummary = dict[str, Any]


def _truncate(s: Optional[str], max_len: int = 255) -> Optional[str]:
    if s is None:
        return None
    return s[:max_len] if len(s) > max_len else s


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
        "external_id": (
            raw.get("external_id") or extract_external_id(raw.get("source_url", ""))
        ),
        "source_url": raw.get("source_url", ""),
        "brand_raw": _truncate(raw.get("brand_raw")),
        "brand_normalized": _truncate(normalize_brand(raw.get("brand_raw"))),
        "model_raw": _truncate(raw.get("model_raw")),
        "model_normalized": _truncate(normalize_model(raw.get("model_raw"))),
        "year": parse_year(raw.get("year_raw")),
        "mileage_km": parse_mileage_km(raw.get("mileage_raw")),
        "price_jpy": parse_price_jpy(raw.get("price_raw")),
        "total_price_jpy": parse_price_jpy(raw.get("total_price_raw")),
        "fuel_raw": _truncate(raw.get("fuel_raw")),
        "fuel_normalized": _truncate(normalize_fuel(raw.get("fuel_raw"))),
        "transmission_raw": _truncate(raw.get("transmission_raw")),
        "transmission_normalized": _truncate(
            normalize_transmission(raw.get("transmission_raw"))
        ),
        "body_type_raw": _truncate(raw.get("body_type_raw")),
        "body_type_normalized": _truncate(
            normalize_body_type(raw.get("body_type_raw"))
        ),
        "location_raw": _truncate(raw.get("location_raw")),
        "location_normalized": _truncate(normalize_location(raw.get("location_raw"))),
        "color_raw": _truncate(raw.get("color_raw")),
        "dealer_name": _truncate(raw.get("dealer_name")),
        "main_image_url": raw.get("main_image_url"),
        "image_urls": raw.get("image_urls") or [],
        "specs": _translate_specs(raw.get("specs_raw") or {}),
    }


def upsert_car(db: Session, data: dict[str, Any]) -> tuple[Car, str]:
    """
    Insert or update car by external_id.
    Returns (car, action) where action is 'inserted' or 'updated'.
    For updates: only overwrite when new value is not None (safer MVP).
    """
    now = datetime.now(timezone.utc)
    existing = db.query(Car).filter(Car.external_id == data["external_id"]).first()

    if existing:
        for k, v in data.items():
            if v is not None:  # Safer: don't overwrite good data with None
                setattr(existing, k, v)
        existing.scraped_at = now
        existing.updated_at = now
        db.commit()
        db.refresh(existing)
        return existing, "updated"

    car = Car(**data, scraped_at=now, updated_at=now)
    db.add(car)
    db.commit()
    db.refresh(car)
    return car, "inserted"


def scrape_brand(
    client: ScraperClient,
    db: Session,
    brand_code: str,
    max_pages: int = 1,
    max_cars: Optional[int] = None,
) -> tuple[list[dict], RunSummary]:
    """Scrape one brand and upsert cars. Returns (results, summary)."""
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

    urls_list = ordered_urls
    if max_cars:
        urls_list = urls_list[:max_cars]

    results = []
    summary: RunSummary = {
        "processed": 0,
        "inserted": 0,
        "updated": 0,
        "failed": 0,
        "skipped": 0,
        "failed_urls": [],
    }

    for detail_url in urls_list:
        try:
            html = client.fetch_html(detail_url)
            raw = parse_detail_page(html, detail_url)
            raw["external_id"] = raw.get("external_id") or extract_external_id(
                detail_url
            )
            if not raw["external_id"]:
                summary["skipped"] += 1
                continue

            normalized = normalize_to_db(raw)
            car, action = upsert_car(db, normalized)
            summary["processed"] += 1
            if action == "inserted":
                summary["inserted"] += 1
            else:
                summary["updated"] += 1
            results.append({"external_id": car.external_id, "id": car.id})
        except Exception as e:  # pylint: disable=broad-except
            db.rollback()
            summary["failed"] += 1
            summary["failed_urls"].append(detail_url)
            print(f"Error scraping {detail_url}: {e}")

    return results, summary


def scrape_all(
    db: Session,
    brands: list[str] | None = None,
    max_pages: int = 1,
    max_cars: Optional[int] = 20,
) -> tuple[list[dict], RunSummary]:
    """Scrape configured brands. Returns (all_results, aggregated_summary)."""
    brands = brands or ["TO"]
    client = ScraperClient()
    all_results = []
    total_summary: RunSummary = {
        "processed": 0,
        "inserted": 0,
        "updated": 0,
        "failed": 0,
        "skipped": 0,
        "failed_urls": [],
    }
    for brand in brands:
        results, summary = scrape_brand(client, db, brand, max_pages, max_cars)
        all_results.extend(results)
        total_summary["processed"] += summary["processed"]
        total_summary["inserted"] += summary["inserted"]
        total_summary["updated"] += summary["updated"]
        total_summary["failed"] += summary["failed"]
        total_summary["skipped"] += summary["skipped"]
        total_summary["failed_urls"].extend(summary["failed_urls"])
    return all_results, total_summary
