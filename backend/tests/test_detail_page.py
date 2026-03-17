"""Tests for detail page parser."""

from conftest import load_fixture
from worker.scraper.parsers.detail_page import parse_detail_page


def test_parses_transmission_from_multi_column_row():
    """Carsensor uses 4-column rows: label1 | value1 | label2 | value2."""
    html = load_fixture("detail_page_multi_column.html")
    result = parse_detail_page(
        html, "https://carsensor.net/usedcar/detail/AU123/index.html"
    )
    assert result["transmission_raw"] == "インパネCVT"
    assert result["location_raw"] == "岡山県岡山市南区"
    assert result["specs_raw"]["ミッション"] == "インパネCVT"
    assert result["specs_raw"]["地域"] == "岡山県岡山市南区"


def test_excludes_junk_rows_from_comparison_tables():
    """Junk labels (values used as keys in comparison/related cars tables) are excluded."""
    html = load_fixture("detail_page_junk_rows.html")
    result = parse_detail_page(
        html, "https://carsensor.net/usedcar/detail/AU456/index.html"
    )
    assert "走行距離" in result["specs_raw"]
    assert "排気量" in result["specs_raw"]
    assert "車検" in result["specs_raw"]
    assert "5.8万km" not in result["specs_raw"]
    assert "1000cc" not in result["specs_raw"]
    assert "2027年（R09）06月" not in result["specs_raw"]
