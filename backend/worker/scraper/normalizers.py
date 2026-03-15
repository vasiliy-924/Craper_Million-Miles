import re
from typing import Optional

from .dictionaries import (
    BODY_TYPE_MAP,
    FUEL_MAP,
    TRANSMISSION_MAP,
    BRAND_MAP,
)


def extract_external_id(url: str) -> Optional[str]:
    """
    Extract AU... from URLs like:
    https://carsensor.net/usedcar/detail/AU6888403167/index.html
    """
    match = re.search(r"/detail/(AU\d+)/", url)
    return match.group(1) if match else None


def normalize_brand(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    return BRAND_MAP.get(value.strip(), value.strip())


def normalize_model(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    return value.strip()


def parse_price_jpy(value: Optional[str]) -> Optional[int]:
    """Parse '149.8 万円' -> 1498000"""
    if not value:
        return None
    match = re.search(r"([\d.]+)\s*万", value)
    if not match:
        return None
    try:
        return int(float(match.group(1)) * 10_000)
    except (ValueError, TypeError):
        return None


def parse_mileage_km(value: Optional[str]) -> Optional[int]:
    """Parse '3.5万km' or '3.5 万km' -> 35000"""
    if not value:
        return None
    match = re.search(r"([\d.]+)\s*万\s*km", value, re.IGNORECASE)
    if not match:
        return None
    try:
        return int(float(match.group(1)) * 10_000)
    except (ValueError, TypeError):
        return None


def parse_year(value: Optional[str]) -> Optional[int]:
    """Parse '2023(R05)' or '2023(R05)年' -> 2023"""
    if not value:
        return None
    match = re.search(r"(\d{4})", value)
    if not match:
        return None
    try:
        return int(match.group(1))
    except (ValueError, TypeError):
        return None


def normalize_fuel(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    return FUEL_MAP.get(value.strip(), value.strip())


def normalize_transmission(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    return TRANSMISSION_MAP.get(value.strip(), value.strip())


def normalize_body_type(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    return BODY_TYPE_MAP.get(value.strip(), value.strip())