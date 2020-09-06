import pytest

from easydata import parsers

data_test_was_price = "Was 99.9€"
data_test_was_price_comma = "Was 99,90"
data_test_was_price_big_dot = "Was 3.330,90"
data_test_was_price_big_comma = "Was 3,330.90"


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Was 99.9€", "99.9"),
        ("", None),
        ("Was €", None),
        ("Was null €", None),
    ],
)
def test_price_text(test_data, result):
    price_parser = parsers.PriceText()
    assert price_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Was 99.9€", 99.9),
        ("Was 99,90", 99.9),
        ("Was 3.330,90", 3330.9),
        ("Was 3,330.90", 3330.9),
        ("Was 0.99 EUR", 0.99),
        (99.9, 99.9),
        (99, 99.0),
        (0, 0.0),
        (0.15, 0.15),
    ],
)
def test_price_float(test_data, result):
    price_parser = parsers.PriceFloat()
    assert price_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "decimals, test_data, result",
    [
        (3, "999.91264", 999.913),
        (3, 999.91264, 999.913),
        (2, "99.91264", 99.91),
        (0, "999.91264", 1000),
        (False, 999.91264215, 999.91264215),
        (None, 999.91264215, 999.91),
    ],
)
def test_price_float_decimals(decimals, test_data, result):
    price_parser = parsers.PriceFloat(decimals=decimals)
    assert price_parser.parse(test_data) == result


def test_price_float_config():
    price_parser = parsers.PriceFloat()
    price_parser.init_config({"ED_PRICE_DECIMALS": 3})
    assert price_parser.parse(999.91264) == 999.913


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Was 99.9€", 99),
        (99.9, 99),
        (99, 99),
        (0.15, 0),
    ],
)
def test_price_int(test_data, result):
    price_parser = parsers.PriceInt()
    assert price_parser.parse(test_data) == result
