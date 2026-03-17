from sqlalchemy.orm import Session

from app.models.car import Car

ALLOWED_SORT = {
    "id",
    "year",
    "mileage_km",
    "price_jpy",
    "brand_normalized",
    "model_normalized",
}


def list_cars(
    db: Session,
    *,
    page: int = 1,
    limit: int = 20,
    brand: str | None = None,
    model: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    min_mileage: int | None = None,
    max_mileage: int | None = None,
    sort_by: str = "id",
    sort_order: str = "asc",
) -> tuple[list[Car], int]:
    """
    Query cars with filters, sorting, and pagination.
    Returns (list of cars for current page, total count).
    """
    query = db.query(Car)

    # --- Apply filters ---
    if brand:
        query = query.filter(Car.brand_normalized.ilike(f"%{brand}%"))
    if model:
        query = query.filter(Car.model_normalized.ilike(f"%{model}%"))
    if min_price is not None:
        query = query.filter(Car.price_jpy >= min_price)
    if max_price is not None:
        query = query.filter(Car.price_jpy <= max_price)
    if min_year is not None:
        query = query.filter(Car.year >= min_year)
    if max_year is not None:
        query = query.filter(Car.year <= max_year)
    if min_mileage is not None:
        query = query.filter(Car.mileage_km >= min_mileage)
    if max_mileage is not None:
        query = query.filter(Car.mileage_km <= max_mileage)

    # --- Count total (before pagination) ---
    total = query.count()

    # --- Sorting ---
    if sort_by not in ALLOWED_SORT:
        sort_by = "id"
    sort_column = getattr(Car, sort_by)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # --- Pagination ---
    offset = (page - 1) * limit
    cars = query.offset(offset).limit(limit).all()

    return cars, total


def get_car_by_id(db: Session, car_id: int) -> Car | None:
    """Get a single car by ID. Returns None if not found."""
    return db.query(Car).filter(Car.id == car_id).first()
