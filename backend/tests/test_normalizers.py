"""Tests for scraper normalizers."""
import pytest

from worker.scraper.normalizers import (
    extract_external_id,
    parse_price_jpy,
    parse_mileage_km,
    parse_year,
    normalize_brand,
    normalize_fuel,
    normalize_transmission,
    normalize_body_type,
    normalize_location,
)


class TestExtractExternalId:
    def test_extracts_au_id_from_url(self):
        url = "https://carsensor.net/usedcar/detail/AU6888403167/index.html"
        assert extract_external_id(url) == "AU6888403167"

    def test_returns_none_for_invalid_url(self):
        assert extract_external_id("https://example.com") is None


class TestParsePriceJpy:
    def test_parses_man_yen(self):
        assert parse_price_jpy("149.8万円") == 1_498_000
        assert parse_price_jpy("263万円") == 2_630_000

    def test_parses_with_space(self):
        assert parse_price_jpy("149.8 万円") == 1_498_000

    def test_does_not_parse_km_as_price(self):
        assert parse_price_jpy("45km") is None

    def test_returns_none_for_empty(self):
        assert parse_price_jpy("") is None
        assert parse_price_jpy(None) is None


class TestParseMileageKm:
    def test_parses_man_km(self):
        assert parse_mileage_km("3.5万km") == 35_000
        assert parse_mileage_km("0.3万km") == 3_000

    def test_parses_plain_km(self):
        assert parse_mileage_km("12km") == 12
        assert parse_mileage_km("300km") == 300

    def test_parses_with_comma(self):
        assert parse_mileage_km("1,200km") == 1_200

    def test_returns_none_for_empty(self):
        assert parse_mileage_km("") is None
        assert parse_mileage_km(None) is None


class TestParseYear:
    def test_parses_year_with_era(self):
        assert parse_year("2023(R05)年") == 2023

    def test_returns_none_for_empty(self):
        assert parse_year("") is None
        assert parse_year(None) is None


class TestNormalizeFuel:
    def test_exact_matches(self):
        assert normalize_fuel("ガソリン") == "petrol"
        assert normalize_fuel("ディーゼル") == "diesel"
        assert normalize_fuel("ハイブリッド") == "hybrid"
        assert normalize_fuel("電気") == "electric"

    def test_pattern_based(self):
        assert normalize_fuel("ガソリン・レギュラー") == "petrol"
        assert normalize_fuel("軽油") == "diesel"

    def test_returns_none_for_empty(self):
        assert normalize_fuel("") is None
        assert normalize_fuel(None) is None


class TestNormalizeTransmission:
    def test_exact_matches(self):
        assert normalize_transmission("フロアCVT") == "CVT"
        assert normalize_transmission("フロアMT") == "MT"

    def test_pattern_based_cvt(self):
        assert normalize_transmission("フロアMTモード付CVT") == "CVT"

    def test_pattern_based_at_mt(self):
        assert normalize_transmission("インパネ4AT") == "AT"
        assert normalize_transmission("フロアMT") == "MT"

    def test_returns_none_for_empty(self):
        assert normalize_transmission("") is None
        assert normalize_transmission(None) is None


class TestNormalizeBodyType:
    def test_exact_matches(self):
        assert normalize_body_type("セダン") == "sedan"
        assert normalize_body_type("ハッチバック") == "hatchback"

    def test_substring_matches(self):
        assert normalize_body_type("クロカン・ＳＵＶ") == "SUV"
        assert normalize_body_type("SUV・クロカン") == "SUV"

    def test_returns_none_for_empty(self):
        assert normalize_body_type("") is None
        assert normalize_body_type(None) is None


class TestNormalizeLocation:
    def test_maps_prefecture(self):
        assert normalize_location("北海道函館市") == "Hokkaido"
        assert normalize_location("愛知県名古屋市港区") == "Aichi"
        assert normalize_location("岡山県岡山市南区") == "Okayama"
        assert normalize_location("静岡県駿東郡") == "Shizuoka"
        assert normalize_location("栃木県宇都宮市") == "Tochigi"
        assert normalize_location("鹿児島県霧島市") == "Kagoshima"
        assert normalize_location("三重県鈴鹿市") == "Mie"

    def test_returns_none_for_unknown(self):
        assert normalize_location("未知の県") is None

    def test_returns_none_for_empty(self):
        assert normalize_location("") is None
        assert normalize_location(None) is None