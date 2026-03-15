from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class CarResponse(BaseModel):
    id: int
    external_id: str
    source_url: str
    brand_raw: Optional[str] = None
    brand_normalized: Optional[str] = None
    model_raw: Optional[str] = None
    model_normalized: Optional[str] = None
    year: Optional[int] = None
    mileage_km: Optional[int] = None
    price_jpy: Optional[int] = None
    total_price_jpy: Optional[int] = None
    location_raw: Optional[str] = None
    location_normalized: Optional[str] = None
    fuel_raw: Optional[str] = None
    fuel_normalized: Optional[str] = None
    transmission_raw: Optional[str] = None
    transmission_normalized: Optional[str] = None
    body_type_raw: Optional[str] = None
    body_type_normalized: Optional[str] = None
    color_raw: Optional[str] = None
    dealer_name: Optional[str] = None
    main_image_url: Optional[str] = None
    image_urls: Optional[list[str]] = None
    specs: Optional[dict[str, Any]] = None
    scraped_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
