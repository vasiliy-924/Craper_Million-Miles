from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.car import Car
from app.models.user import User
from app.schemas.car import CarResponse

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/", response_model=list[CarResponse])
def list_cars(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all cars. Requires authentication."""
    cars = db.query(Car).all()
    return cars


@router.get("/{car_id}", response_model=CarResponse)
def get_car(
    car_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a single car by ID. Requires authentication."""
    car = db.query(Car).filter(Car.id == car_id).first()
    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return car
