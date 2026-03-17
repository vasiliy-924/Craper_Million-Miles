"""Tests for list page parser."""

from conftest import load_fixture
from worker.scraper.parsers.list_page import extract_detail_urls


def test_extracts_detail_urls():
    """HTML with detail links returns full URLs."""
    base = "https://carsensor.net/usedcar/"
    html = load_fixture("list_page_basic.html")
    urls = extract_detail_urls(html, base)
    assert len(urls) == 2
    assert "https://carsensor.net/usedcar/detail/AU123/index.html" in urls
    assert "https://carsensor.net/usedcar/detail/AU456/index.html" in urls


def test_excludes_lease_urls():
    """HTML with /usedcar/lease/ links excludes them."""
    base = "https://carsensor.net/usedcar/"
    html = load_fixture("list_page_with_lease.html")
    urls = extract_detail_urls(html, base)
    assert len(urls) == 1
    assert "AU123" in urls[0]
    assert "lease" not in urls[0].lower()


def test_deduplicates_urls():
    """Same URL twice appears once."""
    base = "https://carsensor.net/"
    html = load_fixture("list_page_with_duplicates.html")
    urls = extract_detail_urls(html, base)
    assert len(urls) == 1
    assert urls[0] == "https://carsensor.net/usedcar/detail/AU123/index.html"


def test_uses_urljoin():
    """Relative href becomes absolute URL with base."""
    base = "https://carsensor.net/usedcar/brand/toyota/"
    html = load_fixture("list_page_rel_url.html")
    urls = extract_detail_urls(html, base)
    assert len(urls) == 1
    assert urls[0] == "https://carsensor.net/usedcar/detail/AU789/index.html"
