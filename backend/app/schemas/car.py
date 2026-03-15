from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


# --- List item: fewer fields for the list view ---
class CarListItemResponse(BaseModel):
    id: int
    external_id: str
    brand_normalized: Optional[str] = None
    model_normalized: Optional[str] = None
    year: Optional[int] = None
    mileage_km: Optional[int] = None
    price_jpy: Optional[int] = None
    main_image_url: Optional[str] = None

    model_config = {"from_attributes": True}


# --- Detail: full car for GET /cars/{id} ---
class CarDetailResponse(BaseModel):
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


# --- Paginated list envelope ---
class CarListResponse(BaseModel):
    items: list[CarListItemResponse]
    total: int
    page: int
    limit: int
    pages: int


# --- Optional: query params as a class (you can also use individual params in the route) ---
class CarListQueryParams(BaseModel):
    page: int = 1
    limit: int = 20
    brand: Optional[str] = None
    model: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    min_mileage: Optional[int] = None
    max_mileage: Optional[int] = None
    sort_by: str = "id"
    sort_order: str = "asc"