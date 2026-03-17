import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.car import CarDetailResponse, CarListItemResponse, CarListResponse
from app.services.cars import get_car_by_id, list_cars

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/", response_model=CarListResponse)
def list_cars_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    brand: str | None = Query(None, description="Filter by brand"),
    model: str | None = Query(None, description="Filter by model"),
    min_price: int | None = Query(None, description="Minimum price (JPY)"),
    max_price: int | None = Query(None, description="Maximum price (JPY)"),
    min_year: int | None = Query(None, description="Minimum year"),
    max_year: int | None = Query(None, description="Maximum year"),
    min_mileage: int | None = Query(None, description="Minimum mileage (km)"),
    max_mileage: int | None = Query(None, description="Maximum mileage (km)"),
    sort_by: str = Query(
        "id", description="Sort field (id, year, mileage_km, price_jpy, etc.)"
    ),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
):
    """List cars with filtering, sorting, and pagination. Requires authentication."""
    cars, total = list_cars(
        db,
        page=page,
        limit=limit,
        brand=brand,
        model=model,
        min_price=min_price,
        max_price=max_price,
        min_year=min_year,
        max_year=max_year,
        min_mileage=min_mileage,
        max_mileage=max_mileage,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    pages = math.ceil(total / limit) if total > 0 else 0
    return CarListResponse(
        items=[CarListItemResponse.model_validate(c) for c in cars],
        total=total,
        page=page,
        limit=limit,
        pages=pages,
    )


@router.get("/{car_id}", response_model=CarDetailResponse)
def get_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single car by ID. Requires authentication."""
    car = get_car_by_id(db, car_id)
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return CarDetailResponse.model_validate(car)
