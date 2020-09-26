import pytest

from easydata import parsers
from easydata.queries import jp, pq
from tests.factory import data_dict, data_html


def test_dict():
    dict_parser = parsers.Dict(
        pq("#size-variants li::items"),
        key_parser=parsers.Text(pq("::text")),
        val_parser=parsers.Bool(pq("::attr(size-stock)"), contains=["true"]),
    )

    expected_result = {"l": True, "xl": False, "xxl": True}
    assert dict_parser.parse(data_html.sizes) == expected_result

    dict_parser = parsers.Dict(
        pq("#size-variants li::items"),
        key_query=pq("::text"),
        val_parser=parsers.Bool(pq("::attr(size-stock)"), contains=["true"]),
    )

    assert dict_parser.parse(data_html.sizes) == expected_result

    dict_parser = parsers.Dict(
        pq("#size-variants li::items"),
        key_query=pq("::text"),
        val_query=pq("::attr(size-stock)"),
    )

    expected_text_result = {"l": "true", "xl": "false", "xxl": "true"}
    assert dict_parser.parse(data_html.sizes) == expected_text_result

    dict_parser = parsers.Dict(
        jp("sizes"), key_parser=parsers.Text(), val_parser=parsers.Bool()
    )

    assert dict_parser.parse(data_dict.sizes) == expected_result

    dict_parser = parsers.Dict(jp("sizes"))

    assert dict_parser.parse(data_dict.sizes) == expected_result

    dict_parser = parsers.Dict(jp("sizes"), key_parser=parsers.Text())

    assert dict_parser.parse(data_dict.sizes) == expected_result

    dict_parser = parsers.Dict(jp("sizes"), val_parser=parsers.Bool())

    assert dict_parser.parse(data_dict.sizes) == expected_result

    dict_parser = parsers.Dict(
        jp("sizes"), key_parser=parsers.Text(), val_parser=parsers.Text()
    )

    expected_result = {"l": "True", "xl": "False", "xxl": "True"}
    assert dict_parser.parse(data_dict.sizes) == expected_result


def test_dict_config():
    dict_parser = parsers.Dict(val_parser=parsers.PriceFloat())

    dict_parser.init_config({"ED_PRICE_DECIMALS": 3})

    assert dict_parser.parse({"price": "123.4537"}) == {"price": 123.454}


def test_dict_config_override():
    dict_parser = parsers.Dict(val_parser=parsers.PriceFloat(decimals=4))

    dict_parser.init_config({"ED_PRICE_DECIMALS": 3})

    assert dict_parser.parse({"price": "123.4537"}) == {"price": 123.4537}


@pytest.mark.parametrize(
    "test_data, result, properties",
    [
        (
            {"sm": "true", "md": "false", "lg": "true"},
            {"sm": "true", "lg": "true"},
            {"key_allow": ["sm", "lg"]},
        ),
        (
            {"sm": "true", "md": "false", "lg": "true"},
            {"sm": "true"},
            {"key_callow": ["sm", "LG"]},
        ),
        (
            {"sm": "true", "md": "false", "lg": "true"},
            {"sm": "true", "lg": "true"},
            {"key_deny": "md"},
        ),
        (
            {"sm": "true", "md": "false", "lg": "true"},
            {"sm": "true", "lg": "true"},
            {"key_cdeny": ["md", "LG"]},
        ),
        (
            {"sm": "true", "md": "false", "lg": "true"},
            {"sm": "true"},
            {"key_allow": ["sm", "lg"], "key_deny": "lg"},
        ),
        (
            {"sm": "true", "md": "false", "lg": None},
            {"sm": "true", "md": "false", "lg": None},
            {},
        ),
        (
            {"sm": "true", "md": "false", "lg": None},
            {"sm": "true", "md": "false"},
            {"ignore_non_values": True},
        ),
        (
            {"sm": "true", None: "false", "lg": "true"},
            {"sm": "true", "lg": "true"},
            {},
        ),
        (
            {"sm": "true", None: "false", "lg": "true"},
            {"sm": "true", None: "false", "lg": "true"},
            {"ignore_non_keys": False},
        ),
    ],
)
def test_dict_variations(test_data, result, properties):
    dict_parser = parsers.Dict(**properties)
    assert dict_parser.parse(test_data) == result


def test_bool_dict():
    bool_dict_parser = parsers.BoolDict(
        pq("#size-variants li::items"),
        key_query=pq("::text"),
        val_query=pq("::attr(size-stock)"),
    )

    expected_text_result = {"l": True, "xl": False, "xxl": True}
    assert bool_dict_parser.parse(data_html.sizes) == expected_text_result


@pytest.mark.parametrize(
    "test_data, result, properties",
    [
        ({"l": True, "xl": False}, {"l": True, "xl": False}, {}),
        ({"l": 12, "xl": 0}, {"l": True, "xl": False}, {}),
        ({"l": "true", "xl": "false"}, {"l": True, "xl": False}, {}),
        ({"l": "True", "xl": "False"}, {"l": True, "xl": False}, {}),
        ({"l": "n/a", "xl": "12"}, {"l": False, "xl": False}, {}),
        (
            {"sm-s": "in-stock", "md-m": "oos", "lg-l": "in-stock"},
            {"sm": True, "md": False, "lg": True},
            {"key_split_text_key": "-", "val_contains": ["in-stock"]},
        ),
        (
            {"sm-s": "in-stock", "md-m": "oos", "lg-l": "in-stock"},
            {"sm": False, "md": False, "lg": False},
            {"key_split_text_key": "-", "val_contains": ["in stock"]},
        ),
        (
            {"sm-s": "in-stock", "md-m": "oos", "lg-l": "in-stock"},
            {"sm": True, "md": False, "lg": True},
            {
                "key_split_text_key": "-",
                "val_contains": ["stock"],
                "val_split_text_key": ("-", -1),
            },
        ),
        (
            {"sm-s": 1, "md-m": 0, "lg-l": 3},
            {"sm": True, "lg": True},
            {"key_split_text_key": "-", "key_allow": ["lg", "sm"]},
        ),
    ],
)
def test_bool_dict_variations(test_data, result, properties):
    bool_dict_parser = parsers.BoolDict(**properties)
    assert bool_dict_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result, properties",
    [
        (
            {"price": "123.4537", "sale_price": "55.2145"},
            {"price": 123.45, "sale_price": 55.21},
            {},
        ),
        (
            {"price": "123.4537", "sale_price": "55.2145"},
            {"price": 123.454, "sale_price": 55.215},
            {"val_decimals": 3},
        ),
        (
            {"price": "123.4537", "sale_price": 1.99},
            {"price": 123.45, "sale_price": None},
            {"val_min_value": 3},
        ),
        (
            {"price": "123.4537", "sale_price": 1.99},
            {"price": 123.45},
            {"val_min_value": 3, "ignore_non_values": True},
        ),
    ],
)
def test_price_float_dict_variations(test_data, result, properties):
    price_dict_parser = parsers.PriceFloatDict(**properties)
    assert price_dict_parser.parse(test_data) == result


def test_price_float_dict_config():
    price_dict_parser = parsers.PriceFloatDict()

    price_dict_parser.init_config({"ED_PRICE_DECIMALS": 3})

    assert price_dict_parser.parse({"price": "123.4537"}) == {"price": 123.454}


def test_price_float_dict_config_override():
    price_dict_parser = parsers.PriceFloatDict(val_decimals=4)

    price_dict_parser.init_config({"ED_PRICE_DECIMALS": 3})

    assert price_dict_parser.parse({"price": "123.4537"}) == {"price": 123.4537}


@pytest.mark.parametrize(
    "test_data, result, properties",
    [
        (
            {"price": "123.4537", "sale_price": "55.2145"},
            {"price": "123.45", "sale_price": "55.21"},
            {},
        ),
        (
            {"price": "123.4537", "sale_price": "1.99"},
            {"price": "123.45"},
            {"val_min_value": 3, "ignore_non_values": True},
        ),
    ],
)
def test_price_text_dict_variations(test_data, result, properties):
    price_dict_parser = parsers.PriceTextDict(**properties)
    assert price_dict_parser.parse(test_data) == result
