"""Tests for scraper pipeline."""
# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.car import Car
from worker.scraper.pipeline import scrape_brand, upsert_car


@pytest.fixture
def db_session():
    """In-memory SQLite for tests."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def test_upsert_inserts_new_row(db_session):
    """First scrape with external_id=X creates one row."""
    data = {
        "external_id": "AU123",
        "source_url": "https://example.com/detail/AU123/",
        "price_jpy": 1_000_000,
        "year": 2020,
    }
    car, action = upsert_car(db_session, data)
    assert action == "inserted"
    assert car.external_id == "AU123"
    assert car.price_jpy == 1_000_000
    assert db_session.query(Car).count() == 1


def test_upsert_updates_existing_row(db_session):
    """Second scrape with same external_id updates values."""
    data1 = {
        "external_id": "AU456",
        "source_url": "https://example.com/detail/AU456/",
        "price_jpy": 1_000_000,
        "year": 2020,
    }
    car1, _ = upsert_car(db_session, data1)
    first_id = car1.id

    data2 = {
        "external_id": "AU456",
        "source_url": "https://example.com/detail/AU456/",
        "price_jpy": 1_200_000,
        "year": 2021,
    }
    car2, action = upsert_car(db_session, data2)
    assert action == "updated"
    assert car2.id == first_id
    assert car2.price_jpy == 1_200_000
    assert car2.year == 2021
    assert db_session.query(Car).count() == 1


def test_no_duplicate_rows(db_session):
    """Same external_id multiple times keeps row count at 1."""
    data = {
        "external_id": "AU789",
        "source_url": "https://example.com/detail/AU789/",
    }
    for _ in range(3):
        upsert_car(db_session, data)
    assert db_session.query(Car).count() == 1


def test_none_does_not_overwrite_existing_value(db_session):
    """Safer policy: new scrape with None for dealer_name keeps old value."""
    data1 = {
        "external_id": "AU999",
        "source_url": "https://example.com/detail/AU999/",
        "dealer_name": "Gulliver",
    }
    upsert_car(db_session, data1)

    data2 = {
        "external_id": "AU999",
        "source_url": "https://example.com/detail/AU999/",
        "dealer_name": None,
    }
    car, _ = upsert_car(db_session, data2)
    assert car.dealer_name == "Gulliver"


def test_partial_failure_does_not_stop_run(db_session):
    """One mocked detail page raises error; others still get processed."""
    client = MagicMock()
    urls = [
        "https://carsensor.net/usedcar/detail/AU111/index.html",
        "https://carsensor.net/usedcar/detail/AU222/index.html",
        "https://carsensor.net/usedcar/detail/AU333/index.html",
    ]

    def fetch_side_effect(url):
        if "AU222" in url:
            raise ValueError("Simulated fetch error")
        return (
            "<html><body><table><tr><th>車台末尾</th><td>1</td></tr>"
            "</table></body></html>"
        )

    client.fetch_html = fetch_side_effect

    with patch("worker.scraper.pipeline.extract_detail_urls", return_value=urls):
        with patch("worker.scraper.pipeline.parse_detail_page") as mock_parse:
            def parse_side_effect(_html, url):
                if "AU222" in url:
                    raise ValueError("Simulated parse error")
                return {
                    "external_id": "AU111" if "AU111" in url else "AU333",
                    "source_url": url,
                }
            mock_parse.side_effect = parse_side_effect

            _results, summary = scrape_brand(
                client, db_session, "TO", max_pages=1, max_cars=3
            )
            assert summary["processed"] >= 2
            assert summary["failed"] >= 1
