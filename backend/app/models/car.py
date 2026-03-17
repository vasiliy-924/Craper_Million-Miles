from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    external_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    source_url: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    brand_raw: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    brand_normalized: Mapped[Optional[str]] = mapped_column(
        String(255),
        index=True,
        nullable=True,
    )
    model_raw: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    model_normalized: Mapped[Optional[str]] = mapped_column(
        String(255),
        index=True,
        nullable=True,
    )
    year: Mapped[Optional[int]] = mapped_column(
        Integer,
        index=True,
        nullable=True,
    )
    mileage_km: Mapped[Optional[int]] = mapped_column(
        Integer,
        index=True,
        nullable=True,
    )
    price_jpy: Mapped[Optional[int]] = mapped_column(
        Integer,
        index=True,
        nullable=True,
    )
    total_price_jpy: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    location_raw: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    location_normalized: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    fuel_raw: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    fuel_normalized: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    transmission_raw: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    transmission_normalized: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    body_type_raw: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    body_type_normalized: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    color_raw: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    dealer_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    main_image_url: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    image_urls: Mapped[Optional[list]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    specs: Mapped[Optional[dict]] = mapped_column(
        JSON,
        default=dict,
        nullable=True,
    )
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
