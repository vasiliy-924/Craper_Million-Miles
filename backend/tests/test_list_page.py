"""Tests for list page parser."""

from worker.scraper.parsers.list_page import extract_detail_urls


def test_extracts_detail_urls():
    """HTML with detail links returns full URLs."""
    base = "https://carsensor.net/usedcar/"
    html = """
    <html>
    <body>
    <a href="/usedcar/detail/AU123/index.html">Car 1</a>
    <a href="/usedcar/detail/AU456/index.html">Car 2</a>
    </body>
    </html>
    """
    urls = extract_detail_urls(html, base)
    assert len(urls) == 2
    assert "https://carsensor.net/usedcar/detail/AU123/index.html" in urls
    assert "https://carsensor.net/usedcar/detail/AU456/index.html" in urls


def test_excludes_lease_urls():
    """HTML with /usedcar/lease/ links excludes them."""
    base = "https://carsensor.net/usedcar/"
    html = """
    <html>
    <body>
    <a href="/usedcar/detail/AU123/index.html">Car</a>
    <a href="/usedcar/lease/detail/AU999/index.html">Lease</a>
    </body>
    </html>
    """
    urls = extract_detail_urls(html, base)
    assert len(urls) == 1
    assert "AU123" in urls[0]
    assert "lease" not in urls[0].lower()


def test_deduplicates_urls():
    """Same URL twice appears once."""
    base = "https://carsensor.net/"
    html = """
    <html>
    <body>
    <a href="/usedcar/detail/AU123/index.html">Car 1</a>
    <a href="/usedcar/detail/AU123/index.html">Car 1 again</a>
    </body>
    </html>
    """
    urls = extract_detail_urls(html, base)
    assert len(urls) == 1
    assert urls[0] == "https://carsensor.net/usedcar/detail/AU123/index.html"


def test_uses_urljoin():
    """Relative href becomes absolute URL with base."""
    base = "https://carsensor.net/usedcar/brand/toyota/"
    html = """
    <html>
    <body>
    <a href="/usedcar/detail/AU789/index.html">Car</a>
    </body>
    </html>
    """
    urls = extract_detail_urls(html, base)
    assert len(urls) == 1
    assert urls[0] == "https://carsensor.net/usedcar/detail/AU789/index.html"
