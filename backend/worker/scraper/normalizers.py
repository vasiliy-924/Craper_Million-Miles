import re
from typing import Optional

from .dictionaries import (
    BODY_TYPE_MAP,
    FUEL_MAP,
    TRANSMISSION_MAP,
    BRAND_MAP,
    PREFECTURE_MAP,
)

_logged_unknowns: set[str] = set()


def _log_unknown(category: str, value: str) -> None:
    """Log unknown values once per run to avoid span."""
    key = f"{category}:{value}"
    if key not in _logged_unknowns:
        _logged_unknowns.add(key)
        print(f"Unknown {category}: {value}")


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
    """Parse '149.8万円', '263万円', '149.8 万円' -> int. Avoid '45km'."""
    if not value:
        return None
    s = value.strip()
    match = re.search(r"([\d.,]+)\s*万\s*円?", s)
    if not match:
        return None
    try:
        num_str = match.group(1).replace(",", "")
        return int(float(num_str) * 10_000)
    except (ValueError, TypeError):
        return None


def parse_mileage_km(value: Optional[str]) -> Optional[int]:
    """Parse '3.5万km' -> 35000, '12km' -> 12, '1,200km' -> 1200"""
    if not value:
        return None
    s = value.strip()
    match = re.search(r"([\d.,]+)\s*万\s*km", s, re.IGNORECASE)
    if match:
        try:
            num_str = match.group(1).replace(",", "")
            return int(float(num_str) * 10_000)
        except (ValueError, TypeError):
            return None
    match = re.search(r"([\d,]+)\s*km", s, re.IGNORECASE)
    if match:
        try:
            num_str = match.group(1).replace(",", "")
            return int(num_str)
        except (ValueError, TypeError):
            return None
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
    s = value.strip()

    result = FUEL_MAP.get(s)
    if result:
        return result

    if "ハイブリッド" in s:
        return "hybrid"
    if "ガソリン" in s or "レギュラー" in s:
        return "petrol"
    if "ディーゼル" in s or "軽油" in s:
        return "diesel"
    if "電気" in s or "EV" in s:
        return "electric"
    _log_unknown("fuel", s)
    return s


def normalize_transmission(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    s = value.strip()
    # 1. Try exact dictionary match first
    result = TRANSMISSION_MAP.get(s)
    if result:
        return result
    # 2. Pattern-based: check substrings (order matters!)
    if "CVT" in s:
        return "CVT"
    if "AT" in s:
        return "AT"
    if "MT" in s:
        return "MT"
    _log_unknown("transmission", s)
    return s


def normalize_body_type(value: Optional[str]) -> Optional[str]:
    if not value or not value.strip():
        return None
    s = value.strip()

    result = BODY_TYPE_MAP.get(s)
    if result:
        return result

    if "SUV" in s or "クロカン" in s:
        return "SUV"
    if "ハッチバック" in s:
        return "hatchback"
    if "ミニバン" in s:
        return "minivan"
    if "セダン" in s or "ワゴン" in s:
        return "sedan"
    if "クーペ" in s:
        return "coupe"
    if "コンパクト" in s:
        return "compact"
    if "軽自動車" in s:
        return "kei"
    if "その他" in s:
        return "other"
    _log_unknown("body_type", s)
    return s


def normalize_location(value: Optional[str]) -> Optional[str]:
    """
    Extract prefecture and map to English.
    e.g. '北海道函館市' -> 'Hokkaido', '愛知県名古屋市港区' -> 'Aichi'
    """
    if not value or not value.strip():
        return None
    s = value.strip()
    for jp, en in PREFECTURE_MAP.items():
        if s.startswith(jp):
            return en
    return None
