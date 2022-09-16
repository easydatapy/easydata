import pytest

import easydata as ed
from tests.factory import data_dict, data_html


@pytest.mark.parametrize(
    "parser, result",
    [
        (
            ed.OR(
                ed.Text(ed.pq(".brand-wrong::text")),
                ed.Text(ed.pq(".brand::text")),
            ),
            "EasyData",
        ),
        (
            ed.OR(
                ed.Text(ed.pq(".brand::text")),
                ed.Text(ed.pq("#name::text")),
            ),
            "EasyData",
        ),
        (
            ed.OR(
                ed.Text(ed.pq(".brand-wrong::text")),
                ed.Text(ed.pq(".brand-wrong-again::text")),
            ),
            None,
        ),
        (
            ed.OR(
                ed.Has(ed.pq(".brand::text"), contains=["WrongData"]),
                ed.Has(ed.pq(".brand::text"), contains=["EasyData"]),
            ),
            True,
        ),
        (
            ed.OR(
                ed.List(ed.pq(".brand-wrong::text-items")),
                ed.Text(ed.pq(".brand::text")),
            ),
            "EasyData",
        ),
    ],
)
def test_or(parser, result):
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    assert parser.parse(test_html) == result


@pytest.mark.parametrize(
    "parser, result",
    [
        (
            ed.OR(
                ed.List(ed.pq(".brand-wrong::text-items")),
                ed.Text(ed.pq(".brand::text")),
                strict_none=True,
            ),
            [],
        ),
        (
            ed.OR(
                ed.Has(ed.pq(".brand::text"), contains=["WrongData"]),
                ed.Has(ed.pq(".brand::text"), default=False, contains=["Wrong2Data"]),
                strict_none=True,
            ),
            False,
        ),
    ],
)
def test_or_strict_none_is_true(parser, result):
    test_html = """
        <p class="brand">EasyData</p>
    """

    assert parser.parse(test_html) == result


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (
            ed.WITH(
                ed.Sentences(
                    ed.pq("#description .features::text"),
                    allow=["date added"],
                ),
                ed.DateTimeSearch(),
            ),
            data_html.features,
            "12/12/2018 10:55:00",
        ),
        (
            ed.WITH(
                ed.Sentences(
                    ed.pq("#description .features::text"),
                    allow=["date added"],
                ),
                ed.Text(split_key=("added:", -1)),
                ed.DateTime(),
            ),
            data_html.features,
            "12/12/2018 10:55:00",
        ),
    ],
)
def test_with(parser, test_data, result):
    assert parser.parse(test_data) == result


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (
            ed.SWITCH(
                ed.Str(ed.jp("brand.name"), uppercase=True),
                ("EASYDATA", "EasyData rules!"),
            ),
            data_dict.item_with_options,
            "EasyData rules!",
        ),
        (
            ed.SWITCH(
                ed.Str(ed.jp("brand.name")),
                ("EASYBOOK", "EasyBook bad!"),
                ("EasyData", "EasyData rules!"),
            ),
            data_dict.item_with_options,
            "EasyData rules!",
        ),
        (
            ed.SWITCH(
                ed.Str(ed.jp("brand.name")),
                ("EASYBOOK", "EasyBook bad!"),
                ("EasyData", ed.Str(ed.jp("title"))),
            ),
            data_dict.item_with_options,
            "EasyBook pro 15",
        ),
        (
            ed.SWITCH(
                ed.Str(ed.jp("brand.name")),
                ("EASYBOOK", "EasyBook bad!"),
                ("EASYDATA", "EasyData rules!"),
            ),
            data_dict.item_with_options,
            None,
        ),
        (
            ed.SWITCH(
                ed.Str(ed.jp("brand.name")),
                ("EASYBOOK", "EasyBook bad!"),
                ("EASYDATA", "EasyData rules!"),
                default="Hello!",
            ),
            data_dict.item_with_options,
            "Hello!",
        ),
        (
            ed.SWITCH(
                ed.Str(ed.jp("brand.name")),
                ("EASYBOOK", "EasyBook bad!"),
                ("EASYDATA", "EasyData rules!"),
                default=ed.Str(ed.jp("title")),
            ),
            data_dict.item_with_options,
            "EasyBook pro 15",
        ),
    ],
)
def test_switch(parser, test_data, result):
    assert parser.parse(test_data) == result


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (
            ed.IF(
                ed.Str(ed.jp("brand.name")),
                ("Hello", "There"),
            ),
            data_dict.item_with_options,
            ("Hello", "There"),
        ),
        (
            ed.IF(
                ed.Str(ed.jp("brand.name2")),
                then_parser=ed.Str(ed.jp("brand.origin")),
                else_parser=ed.Str(ed.jp("title")),
            ),
            data_dict.item_with_options,
            "EasyBook pro 15",
        ),
        (
            ed.IF(
                ed.Float(ed.jp("price")),
                condition=lambda price_value: price_value > 50,
                then_parser=ed.Float(ed.jp("sale_price")),
            ),
            data_dict.item_with_options,
            49.99,
        ),
        (
            ed.IF(
                ed.Float(ed.jp("price")),
                condition=lambda price_value: price_value > 100,
                then_parser=ed.Float(ed.jp("sale_price")),
            ),
            data_dict.item_with_options,
            None,
        ),
        (
            ed.IF(
                ed.Float(ed.jp("price22")),
                then_parser=ed.Float(ed.jp("sale_price")),
            ),
            data_dict.item_with_options,
            None,
        ),
    ],
)
def test_if(parser, test_data, result):
    assert parser.parse(test_data) == result
