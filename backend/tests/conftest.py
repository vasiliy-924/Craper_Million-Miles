"""Pytest fixtures for API tests. Uses Testcontainers (local) or compose db (Docker)."""

import os
import pathlib

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

# Set env before app imports so Settings loads test values
os.environ.setdefault(
    "DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/test"
)
os.environ.setdefault("JWT_SECRET", "test-secret-for-pytest")

from app.core.security import hash_password  # noqa: E402
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.car import Car
from app.models.user import User

FIXTURES_DIR = pathlib.Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> str:
    """Load HTML fixture from tests/fixtures/."""
    path = FIXTURES_DIR / name
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for the test session (local only)."""
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def test_engine(request):
    """Create SQLAlchemy engine. Uses compose db when USE_EXISTING_DB=1 (Docker)."""
    use_existing = os.environ.get("USE_EXISTING_DB", "").strip() in ("1", "true", "yes")
    if use_existing:
        url = os.environ["DATABASE_URL"]
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        yield engine
    else:
        postgres = request.getfixturevalue("postgres_container")
        url = postgres.get_connection_url()
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        yield engine


@pytest.fixture(scope="session")
def SessionFactory(test_engine):
    """Session factory for test DB."""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def db_session(SessionFactory, test_engine):
    """Per-test DB session. Uses transaction rollback for isolation."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = SessionFactory(bind=connection)

    existing = session.query(User).filter(User.username == "admin").first()
    if not existing:
        admin = User(
            username="admin",
            password_hash=hash_password("admin123"),
        )
        session.add(admin)
    session.flush()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    """TestClient with overridden get_db."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Bearer token headers for authenticated requests."""
    resp = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _make_car(**kwargs) -> dict:
    """Factory for car data."""
    defaults = {
        "external_id": "AU123",
        "source_url": "https://carsensor.net/usedcar/detail/AU123/index.html",
        "brand_raw": "トヨタ",
        "brand_normalized": "Toyota",
        "model_raw": "カムリ",
        "model_normalized": "Camry",
        "year": 2020,
        "mileage_km": 35000,
        "price_jpy": 1_500_000,
        "location_raw": "愛知県",
        "location_normalized": "Aichi",
    }
    defaults.update(kwargs)
    return defaults


@pytest.fixture
def sample_cars(db_session):
    """Insert sample cars for list/detail tests."""
    cars_data = [
        _make_car(
            external_id="AU001",
            brand_normalized="Toyota",
            year=2020,
            price_jpy=1_000_000,
        ),
        _make_car(
            external_id="AU002",
            brand_normalized="Honda",
            year=2021,
            price_jpy=1_500_000,
        ),
        _make_car(
            external_id="AU003",
            brand_normalized="Toyota",
            year=2022,
            price_jpy=2_000_000,
        ),
    ]
    cars = []
    for d in cars_data:
        car = Car(**d)
        db_session.add(car)
        cars.append(car)
    db_session.flush()
    for c in cars:
        db_session.refresh(c)
    return cars
