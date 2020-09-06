import pytest

from easydata.utils import price


@pytest.mark.parametrize(
    "test_data, result",
    [("Was 99.99 $", 99.99), ("Was 99.9924$", 99.99), ("Was 25", 25.0)],
)
def test_to_float(test_data, result):
    assert price.to_float(test_data) == result


@pytest.mark.parametrize(
    "test_data, decimals, result",
    [
        ("Was 25.9924", 3, 25.992),
        ("Was 25.9926", 3, 25.993),
        ("Was 25.9924", False, 25.9924),
    ],
)
def test_to_float_decimals(test_data, decimals, result):
    assert price.to_float(test_data, decimals=decimals) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Was 99.99 $", "99.99"),
    ],
)
def test_to_string(test_data, result):
    assert price.to_string(test_data) == result


@pytest.mark.parametrize(
    "normal_price, sale_price, decimals, discount",
    [
        (100, 30, 2, 70.0),
        (100, 30, 2, 70.0),
        (29.99, 21.99, 2, 26.68),
        (29.99, 21.99, 1, 26.7),
    ],
)
def test_get_discount(normal_price, sale_price, decimals, discount):
    assert price.get_discount(normal_price, sale_price, decimals) == discount


@pytest.mark.parametrize("normal_price, sale_price, discount", [(29.99, 21.99, 27)])
def test_get_discount_no_decimals(normal_price, sale_price, discount):
    assert price.get_discount(normal_price, sale_price, no_decimals=True) == discount
