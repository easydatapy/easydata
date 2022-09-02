import pytest

import easydata as ed


@pytest.mark.parametrize(
    "parser,test_data,result",
    [
        (ed.PriceText(), "Was 99.9€", "99.9"),
        (ed.PriceText(), "", None),
        (ed.PriceText(), "Was €", None),
        (ed.PriceText(), "Was null €", None),
        (ed.PriceFloat(), "Was 99.9€", 99.9),
        (ed.PriceFloat(), "Was 99,90", 99.90),
        (ed.PriceFloat(), "Was 99,9092", 99.9092),
        (ed.PriceFloat(), "Was 99,9099", 99.9099),
        (ed.PriceFloat(), "Was 3.330,90", 3330.90),
        (ed.PriceFloat(), "Was 3,330.90", 3330.90),
        (ed.PriceFloat(), "Was 3330.90", 3330.90),
        (ed.PriceFloat(), "Was 0.99 EUR", 0.99),
        (ed.PriceFloat(), 99.9, 99.9),
        (ed.PriceFloat(), 99, 99.0),
        (ed.PriceFloat(), 0, 0.0),
        (ed.PriceFloat(), 0.15, 0.15),
        (ed.PriceFloat(decimals=3), "999.91264", 999.913),
        (ed.PriceFloat(decimals=3), 999.91264, 999.913),
        (ed.PriceFloat(decimals=2), "99.91264", 99.91),
        (ed.PriceFloat(decimals=0), "999.91264", 1000),
        (ed.PriceFloat(decimals=None), 999.91264215, 999.91264215),
        (ed.PriceFloat(min_value=10), "15.99", 15.99),
        (ed.PriceFloat(min_value=10), "10", 10.0),
        (ed.PriceFloat(min_value=10), "9.99", None),
        (ed.PriceFloat(min_value=10), None, None),
        (ed.PriceFloat(min_value=10), 0, None),
        (ed.PriceFloat(min_value=10), "Was null €", None),
        (ed.PriceFloat(max_value=10), "9.99", 9.99),
        (ed.PriceFloat(max_value=10), "10", 10.0),
        (ed.PriceFloat(max_value=10), "15.99", None),
        (ed.PriceFloat(max_value=10), None, None),
        (ed.PriceFloat(max_value=10), 0, 0),
        (ed.PriceFloat(max_value=10), "Was null €", None),
        (ed.PriceFloat(min_value=10, max_value=16), "15.99", 15.99),
        (ed.PriceFloat(min_value=10, max_value=15), "15.99", None),
        (ed.PriceFloat(min_value=10, max_value=16, decimals=1), "15.12", 15.1),
        (ed.PriceFloat(decimal_separator=None), "Was 3330.123", 3330123.0),
        (ed.PriceFloat(decimal_separator="."), "Was 3330.123", 3330.123),
        (ed.PriceInt(), "Was 99.9€", 99),
        (ed.PriceInt(), 99.9, 99),
        (ed.PriceInt(), 99, 99),
        (ed.PriceInt(), 0.15, 0),
    ],
)
def test_price(parser, test_data, result):
    assert parser.parse(test_data) == result


@pytest.mark.parametrize(
    "config_name, config_value, test_data, result",
    [
        ("ED_PRICE_DECIMALS", 3, 999.91264, 999.913),
        ("ED_PRICE_MIN_VALUE", 10, 9.99, None),
        ("ED_PRICE_MAX_VALUE", 14, "15.99", None),
    ],
)
def test_price_float_config(config_name, config_value, test_data, result):
    parser = ed.PriceFloat()
    parser.init_config({config_name: config_value})

    assert parser.parse(test_data) == result
