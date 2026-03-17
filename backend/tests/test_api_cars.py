"""API tests for cars endpoints."""


def test_list_cars_requires_auth(client):
    """GET /cars without token returns 401."""
    resp = client.get("/cars")
    assert resp.status_code == 401


def test_list_cars_returns_paginated(client, auth_headers, sample_cars):
    """GET /cars with token returns 200 and paginated response."""
    resp = client.get("/cars", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "pages" in data
    assert data["total"] >= 3
    assert len(data["items"]) >= 3


def test_list_cars_filter_by_brand(client, auth_headers, sample_cars):
    """GET /cars?brand=Toyota returns only Toyota cars."""
    resp = client.get("/cars", headers=auth_headers, params={"brand": "Toyota"})
    assert resp.status_code == 200
    data = resp.json()
    for item in data["items"]:
        assert item["brand_normalized"] == "Toyota"


def test_list_cars_filter_by_price(client, auth_headers, sample_cars):
    """GET /cars?min_price=X&max_price=Y returns filtered cars."""
    resp = client.get(
        "/cars",
        headers=auth_headers,
        params={"min_price": 1_200_000, "max_price": 1_800_000},
    )
    assert resp.status_code == 200
    data = resp.json()
    for item in data["items"]:
        if item.get("price_jpy") is not None:
            assert 1_200_000 <= item["price_jpy"] <= 1_800_000


def test_list_cars_sort(client, auth_headers, sample_cars):
    """GET /cars?sort_by=price_jpy&sort_order=desc returns correct order."""
    resp = client.get(
        "/cars",
        headers=auth_headers,
        params={"sort_by": "price_jpy", "sort_order": "desc"},
    )
    assert resp.status_code == 200
    data = resp.json()
    items = data["items"]
    if len(items) >= 2:
        prices = [i.get("price_jpy") for i in items if i.get("price_jpy") is not None]
        assert prices == sorted(prices, reverse=True)


def test_list_cars_pagination(client, auth_headers, sample_cars):
    """GET /cars?page=2&limit=2 returns correct page slice."""
    resp = client.get(
        "/cars",
        headers=auth_headers,
        params={"page": 2, "limit": 2},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["page"] == 2
    assert data["limit"] == 2
    assert len(data["items"]) <= 2


def test_get_car_detail_success(client, auth_headers, sample_cars):
    """GET /cars/{id} with valid id returns 200 and full car data."""
    car_id = sample_cars[0].id
    resp = client.get(f"/cars/{car_id}", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == car_id
    assert data["external_id"] == "AU001"
    assert data["brand_normalized"] == "Toyota"
    assert "source_url" in data
    assert "specs" in data


def test_get_car_detail_not_found(client, auth_headers):
    """GET /cars/99999 returns 404."""
    resp = client.get("/cars/99999", headers=auth_headers)
    assert resp.status_code == 404


def test_get_car_detail_requires_auth(client, sample_cars):
    """GET /cars/{id} without token returns 401."""
    car_id = sample_cars[0].id
    resp = client.get(f"/cars/{car_id}")
    assert resp.status_code == 401
