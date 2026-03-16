"""Tests for detail page parser."""
import pytest

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
    result = parse_detail_page(html, "https://carsensor.net/usedcar/detail/AU123/index.html")
    assert result["transmission_raw"] == "インパネCVT"
    assert result["location_raw"] == "岡山県岡山市南区"
    assert result["specs_raw"]["ミッション"] == "インパネCVT"
    assert result["specs_raw"]["地域"] == "岡山県岡山市南区"
