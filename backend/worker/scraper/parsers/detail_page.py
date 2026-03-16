"""Parse car detail pages from carsensor.net."""
import re
from typing import Any
from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_detail_page(html: str, source_url: str) -> dict[str, Any]:
    """
    Parse a car detail page and return raw extracted fields.
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {
        "external_id": None,
        "source_url": source_url,
        "brand_raw": None,
        "model_raw": None,
        "price_raw": None,
        "total_price_raw": None,
        "year_raw": None,
        "mileage_raw": None,
        "fuel_raw": None,
        "transmission_raw": None,
        "body_type_raw": None,
        "dealer_name": None,
        "main_image_url": None,
        "image_urls": [],
        "specs_raw": {},
        "location_raw": None,
        "color_raw": None,
    }

    # Extract external_id from URL
    match = re.search(r"/detail/(AU\d+)/", source_url)
    if match:
        result["external_id"] = match.group(1)

    # Title often contains brand and model (e.g. "ホンダ N-BOX カスタム 660 L")
    title_el = soup.find("h1")
    if title_el:
        title = title_el.get_text(strip=True)
        parts = title.split()
        if parts:
            result["brand_raw"] = parts[0]
        if len(parts) > 1:
            result["model_raw"] = " ".join(parts[1:])

    # Parse all tables - carsensor uses tables for specs and prices
    # Rows can have 2 cells (label, value) or 4+ cells (label1, value1, label2, value2, ...)
    for row in soup.find_all("tr"):
        cells = row.find_all(["th", "td"])
        if len(cells) < 2:
            continue
        # Process each label-value pair in the row
        for i in range(0, len(cells) - 1, 2):
            label = cells[i].get_text(strip=True)
            value = cells[i + 1].get_text(strip=True)
            if not label:
                continue
            result["specs_raw"][label] = value

            if "年式" in label or "初度登録" in label:
                result["year_raw"] = value
            if "走行距離" in label:
                result["mileage_raw"] = value
            if "ミッション" in label:
                result["transmission_raw"] = value
            if "エンジン種別" in label:
                result["fuel_raw"] = value
            if "ボディタイプ" in label:
                result["body_type_raw"] = value
            if "車両本体価格" in label or ("本体価格" in label and "車両" in label):
                result["price_raw"] = value
            if "支払総額" in label and "税込" in label:
                result["total_price_raw"] = value
            if "販売地域" in label or "所在地" in label or "都道府県" in label or "地域" in label:
                result["location_raw"] = value
            if "色" in label:
                result["color_raw"] = value
            elif "支払総額" in label and not result["total_price_raw"]:
                result["total_price_raw"] = value

    # Fallback: populate from specs_raw if not set during table loop
    # (Carsensor may use different table structures or label variants)
    if not result["location_raw"]:
        for key in ("地域", "販売地域", "所在地", "都道府県"):
            if key in result["specs_raw"]:
                result["location_raw"] = result["specs_raw"][key]
                break
    if not result["transmission_raw"]:
        for key in result["specs_raw"]:
            if "ミッション" in key or "変速" in key:
                result["transmission_raw"] = result["specs_raw"][key]
                break
    if not result["color_raw"]:
        for key in result["specs_raw"]:
            if key == "色" or "色" in key:
                result["color_raw"] = result["specs_raw"][key]
                break

    # Fallback: if price not in table, scan for "X.X万円" near "本体" text
    if not result["price_raw"]:
        page_text = soup.get_text()
        for match in re.finditer(r"([\d.]+)\s*万円", page_text):
            # Check if this appears near 車両本体 or 本体価格 (within ~50 chars)
            start = max(0, match.start() - 50)
            context = page_text[start: match.end() + 20]
            if "本体" in context or "車両" in context:
                result["price_raw"] = match.group(0)
                break

    # Dealer name - first link to /shop/
    dealer_link = soup.find("a", href=lambda h: h and "/shop/" in str(h))
    if dealer_link:
        result["dealer_name"] = dealer_link.get_text(strip=True)

    # Collect car images and keep the first one as the main image.
    seen_images = set()
    for img in soup.find_all("img", src=True):
        src = img.get("src", "").strip()
        if not src:
            continue
        if "usedcar" not in src and "carsensor" not in src:
            continue

        full_src = urljoin(source_url, src)
        if full_src in seen_images:
            continue

        seen_images.add(full_src)
        result["image_urls"].append(full_src)

    if result["image_urls"]:
        result["main_image_url"] = result["image_urls"][0]

    return result
