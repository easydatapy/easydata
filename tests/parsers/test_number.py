import pytest

from easydata import parsers


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Was 99.9€", "99.9"),
        ("1224,24", "1224.24"),
        ("", None),
        ("Was €", None),
        ("Was null €", None),
    ],
)
def test_float_text(test_data, result):
    assert parsers.FloatText().parse(test_data) == result


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
def test_float(test_data, result):
    assert parsers.Float().parse(test_data) == result


@pytest.mark.parametrize(
    "decimals, test_data, result",
    [
        (3, "999.91264", 999.913),
        (3, 999.91264, 999.913),
        (2, "99.91264", 99.91),
        (0, "999.91264", 1000),
        (False, 999.91264215, 999.91264215),
        (None, 999.91264215, 999.91264215),
    ],
)
def test_float_decimals(decimals, test_data, result):
    assert parsers.Float(decimals=decimals).parse(test_data) == result


@pytest.mark.parametrize(
    "min_value, test_data, result",
    [
        (10, "15.99", 15.99),
        (10, "10", 10.0),
        (10, "9.99", None),
        (10, None, None),
        (10, 0, None),
        (10, "Was null €", None),
    ],
)
def test_float_min_value(min_value, test_data, result):
    assert parsers.Float(min_value=min_value).parse(test_data) == result


@pytest.mark.parametrize(
    "max_value, test_data, result",
    [
        (10, "9.99", 9.99),
        (10, "10", 10.0),
        (10, "15.99", None),
        (10, None, None),
        (10, 0, 0),
        (10, "Was null €", None),
    ],
)
def test_float_max_value(max_value, test_data, result):
    assert parsers.Float(max_value=max_value).parse(test_data) == result


@pytest.mark.parametrize(
    "config_name, config_value, test_data, result",
    [
        ("ED_NUMBER_DECIMALS", 3, 999.91264, 999.913),
        ("ED_NUMBER_MIN_VALUE", 10, 9.99, None),
        ("ED_NUMBER_MAX_VALUE", 14, "15.99", None),
    ],
)
def test_float_config(config_name, config_value, test_data, result):
    float_parser = parsers.Float()
    float_parser.init_config({config_name: config_value})

    assert float_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Was 99.9€", 99),
        (99.9, 99),
        (99, 99),
        (0.15, 0),
    ],
)
def test_int(test_data, result):
    assert parsers.PriceInt().parse(test_data) == result
