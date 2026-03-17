"""Tests for detail page parser."""

from worker.scraper.parsers.detail_page import parse_detail_page


def test_parses_transmission_from_multi_column_row():
    """Carsensor uses 4-column rows: label1 | value1 | label2 | value2."""
    html = """
    <html>
    <body>
    <table>
    <tr>
        <th>車台末尾番号</th><td>867</td>
        <th>ミッション</th><td>インパネCVT</td>
    </tr>
    <tr>
        <th>地域</th><td>岡山県岡山市南区</td>
    </tr>
    </table>
    </body>
    </html>
    """
    result = parse_detail_page(
        html, "https://carsensor.net/usedcar/detail/AU123/index.html"
    )
    assert result["transmission_raw"] == "インパネCVT"
    assert result["location_raw"] == "岡山県岡山市南区"
    assert result["specs_raw"]["ミッション"] == "インパネCVT"
    assert result["specs_raw"]["地域"] == "岡山県岡山市南区"


def test_excludes_junk_rows_from_comparison_tables():
    """Junk labels (values used as keys in comparison/related cars tables) are excluded."""
    html = """
    <html>
    <body>
    <table>
    <tr>
        <th>走行距離</th><td>4.3万km</td>
        <th>5.8万km</th><td>12km</td>
    </tr>
    <tr>
        <th>排気量</th><td>1000cc</td>
        <th>1000cc</th><td>1500cc</td>
    </tr>
    <tr>
        <th>車検</th><td>2027年（R09）04月</td>
        <th>2027年（R09）06月</th><td>2026年（R08）10月</td>
    </tr>
    </table>
    </body>
    </html>
    """
    result = parse_detail_page(
        html, "https://carsensor.net/usedcar/detail/AU456/index.html"
    )
    assert "走行距離" in result["specs_raw"]
    assert "排気量" in result["specs_raw"]
    assert "車検" in result["specs_raw"]
    assert "5.8万km" not in result["specs_raw"]
    assert "1000cc" not in result["specs_raw"]
    assert "2027年（R09）06月" not in result["specs_raw"]
