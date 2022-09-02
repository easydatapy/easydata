import pytest

import easydata as ed
from tests.factory import data_dict, data_html

EXPECTED_DICT_RESULT = {"l": True, "xl": False, "xxl": True}


@pytest.mark.parametrize(
    "dict_parser, test_data, results",
    [
        (
            ed.Dict(
                ed.pq("#size-variants li::items"),
                key_parser=ed.Text(ed.pq("::text")),
                val_parser=ed.Bool(
                    ed.pq("::attr(size-stock)"),
                    contains=["true"],
                ),
            ),
            data_html.sizes,
            EXPECTED_DICT_RESULT,
        ),
        (
            ed.Dict(
                ed.pq("#size-variants li::items"),
                key_query=ed.pq("::text"),
                val_parser=ed.Bool(
                    ed.pq("::attr(size-stock)"),
                    contains=["true"],
                ),
            ),
            data_html.sizes,
            EXPECTED_DICT_RESULT,
        ),
        (
            ed.Dict(
                ed.pq("#size-variants li::items"),
                key_query=ed.pq("::text"),
                val_query=ed.pq("::attr(size-stock)"),
            ),
            data_html.sizes,
            {"l": "true", "xl": "false", "xxl": "true"},
        ),
        (
            ed.Dict(
                ed.jp("sizes"),
                key_parser=ed.Text(),
                val_parser=ed.Bool(),
            ),
            data_dict.sizes,
            EXPECTED_DICT_RESULT,
        ),
        (
            ed.Dict(ed.jp("sizes")),
            data_dict.sizes,
            EXPECTED_DICT_RESULT,
        ),
        (
            ed.Dict(
                ed.jp("sizes"),
                key_parser=ed.Text(),
            ),
            data_dict.sizes,
            EXPECTED_DICT_RESULT,
        ),
        (
            ed.Dict(
                ed.jp("sizes"),
                val_parser=ed.Bool(),
            ),
            data_dict.sizes,
            EXPECTED_DICT_RESULT,
        ),
        (
            ed.Dict(
                ed.jp("sizes"),
                key_parser=ed.Text(),
                val_parser=ed.Text(),
            ),
            data_dict.sizes,
            {"l": "True", "xl": "False", "xxl": "True"},
        ),
        (
            ed.Dict(
                val_parser=ed.PriceFloat(),
            ).init_config({"ED_PRICE_DECIMALS": 3}),
            {"price": "123.4537"},
            {"price": 123.454},
        ),
        (
            ed.Dict(
                val_parser=ed.PriceFloat(decimals=2),
            ).init_config({"ED_PRICE_DECIMALS": 3}),
            {"price": "123.4537"},
            {"price": 123.45},
        ),
    ],
)
def test_dict(dict_parser, test_data, results):
    assert dict_parser.parse(test_data) == results


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
        (
            {"sm": "true", "md": "false", "lg": "true"},
            {"sm": "sm", "md": "md", "lg": "lg"},
            {"dict_val_from_key": True},
        ),
    ],
)
def test_dict_variations(test_data, result, properties):
    dict_parser = ed.Dict(**properties)
    assert dict_parser.parse(test_data) == result


def test_bool_dict():
    bool_dict_parser = ed.BoolDict(
        ed.pq("#size-variants li::items"),
        key_query=ed.pq("::text"),
        val_query=ed.pq("::attr(size-stock)"),
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
    bool_dict_parser = ed.BoolDict(**properties)
    assert bool_dict_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (
            ed.PriceFloatDict(),
            {"price": "123.4537", "sale_price": "55.2145"},
            {"price": 123.4537, "sale_price": 55.2145},
        ),
        (
            ed.PriceFloatDict(val_decimals=3),
            {"price": "123.4537", "sale_price": "55.2145"},
            {"price": 123.454, "sale_price": 55.215},
        ),
        (
            ed.PriceFloatDict(val_min_value=3),
            {"price": "123.4537", "sale_price": 1.99},
            {"price": 123.4537, "sale_price": None},
        ),
        (
            ed.PriceFloatDict(
                val_min_value=3,
                ignore_non_values=True,
                val_decimals=2,
            ),
            {"price": "123.4537", "sale_price": 1.99},
            {"price": 123.45},
        ),
        (
            ed.PriceFloatDict().init_config({"ED_PRICE_DECIMALS": 3}),
            {"price": "123.4537"},
            {"price": 123.454},
        ),
        (
            ed.PriceFloatDict(
                val_decimals=4,
            ).init_config({"ED_PRICE_DECIMALS": 3}),
            {"price": "123.4537"},
            {"price": 123.4537},
        ),
        (
            ed.PriceTextDict(),
            {"price": "123.4537", "sale_price": "55.2145"},
            {"price": "123.4537", "sale_price": "55.2145"},
        ),
        (
            ed.PriceTextDict(
                val_decimals=2,
                val_min_value=3,
                ignore_non_values=True,
            ),
            {"price": "123.4537", "sale_price": "1.99"},
            {"price": "123.45"},
        ),
    ],
)
def test_price_dict_variations(parser, test_data, result):
    assert parser.parse(test_data) == result
