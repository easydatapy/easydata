import pytest

import easydata as ed
from easydata.data import DataBag
from tests.factory import data_html


@pytest.mark.parametrize(
    "test_parsers, result",
    [
        (
            (
                ed.Text(ed.pq(".brand-wrong::text")),
                ed.Text(ed.pq(".brand::text")),
            ),
            "EasyData",
        ),
        (
            (
                ed.Text(ed.pq(".brand::text")),
                ed.Text(ed.pq("#name::text")),
            ),
            "EasyData",
        ),
        (
            (
                ed.Text(ed.pq(".brand-wrong::text")),
                ed.Text(ed.pq(".brand-wrong-again::text")),
            ),
            None,
        ),
        (
            (
                ed.Bool(ed.pq(".brand::text"), contains=["WrongData"]),
                ed.Bool(ed.pq(".brand::text"), contains=["EasyData"]),
            ),
            True,
        ),
        (
            (
                ed.List(ed.pq(".brand-wrong::text-items")),
                ed.Text(ed.pq(".brand::text")),
            ),
            "EasyData",
        ),
    ],
)
def test_or(test_parsers, result):
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    or_parser = ed.Or(*test_parsers)
    assert or_parser.parse(test_html) == result


@pytest.mark.parametrize(
    "test_parsers, result",
    [
        (
            (
                ed.List(ed.pq(".brand-wrong::text-items")),
                ed.Text(ed.pq(".brand::text")),
            ),
            [],
        ),
        (
            (
                ed.Bool(ed.pq(".brand::text"), contains=["WrongData"]),
                ed.Bool(ed.pq(".brand::text"), default=False, contains=["Wrong2Data"]),
            ),
            False,
        ),
    ],
)
def test_or_strict_none_is_true(test_parsers, result):
    test_html = """
        <p class="brand">EasyData</p>
    """

    or_parser = ed.Or(
        *test_parsers,
        strict_none=True,
    )
    assert or_parser.parse(test_html) == result


def test_with():
    with_parser = ed.With(
        ed.Sentences(
            ed.pq("#description .features::text"),
            allow=["date added"],
        ),
        ed.DateTimeSearch(),
    )
    assert with_parser.parse(data_html.features) == "12/12/2018 10:55:00"

    assert (
        ed.With(
            ed.Sentences(
                ed.pq("#description .features::text"),
                allow=["date added"],
            ),
            ed.Text(split_key=("added:", -1)),
            ed.DateTime(),
        ).parse(data_html.features)
        == "12/12/2018 10:55:00"
    )


def test_join_text():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    join_text_parser = ed.ConcatText(
        ed.Text(ed.pq(".brand::text")),
        ed.Text(ed.pq("#name::text")),
    )
    assert join_text_parser.parse(test_html) == "EasyData Easybook Pro 13"

    join_text_parser = ed.ConcatText(
        ed.Text(ed.pq(".brand-wrong-selector::text")),
        ed.Text(ed.pq("#name::text")),
    )
    assert join_text_parser.parse(test_html) == "Easybook Pro 13"


def test_join_text_custom_separator():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    assert (
        ed.ConcatText(
            ed.Text(ed.pq(".brand::text")),
            ed.Text(ed.pq("#name::text")),
            separator="-",
        ).parse(test_html)
        == "EasyData-Easybook Pro 13"
    )


def test_join_list():
    test_dict = {"features": ["gold color", "retina"], "specs": ["i7 proc", "16 gb"]}

    join_list_parser = ed.JoinList(
        ed.List(ed.jp("features"), parser=ed.Text()),
        ed.List(ed.jp("specs"), parser=ed.Text()),
    )

    expected_result = ["gold color", "retina", "i7 proc", "16 gb"]

    assert join_list_parser.parse(test_dict) == expected_result


def test_join_dict():
    test_dict = {
        "features": {"color": "gold", "display": "retina"},
        "specs": {"proc": "i7", "ram": "16 gb"},
    }

    join_dict_parser = ed.MergeDict(
        ed.Dict(
            ed.jp("features"),
            key_parser=ed.Text(),
            val_parser=ed.Text(),
        ),
        ed.Dict(
            ed.jp("specs"),
            key_parser=ed.Text(),
            val_parser=ed.Text(),
        ),
    )

    expected_result = {
        "color": "gold",
        "display": "retina",
        "proc": "i7",
        "ram": "16 gb",
    }
    assert join_dict_parser.parse(test_dict) == expected_result


@pytest.mark.parametrize(
    "ignore_non_values, result",
    [
        (False, {"brand": None, "color": "gold", "ram": "16 gb"}),
        (True, {"color": "gold", "ram": "16 gb"}),
    ],
)
def test_item_dict(ignore_non_values, result):
    test_features_dict = {"color": "gold", "display": "retina"}
    test_specs_dict = {"proc": "i7", "ram": "16 gb"}

    item_dict_parser = ed.ItemDict(
        ignore_non_values=ignore_non_values,
        color=ed.Text(ed.jp("color")),
        ram=ed.Text(ed.jp("ram"), source="specs"),
        brand=ed.Text(ed.jp("features.brand")),
    )

    data_bag = DataBag(main=test_features_dict, specs=test_specs_dict)
    assert item_dict_parser.parse(data_bag) == result


def test_item_dict_exception_on_non_values():
    item_dict_parser = ed.ItemDict(
        exception_on_non_values=True,
        color=ed.Text(ed.jp("color")),
        brand=ed.Text(ed.jp("features.brand")),
    )

    with pytest.raises(ValueError):
        item_dict_parser.parse({"color": "gold"})


@pytest.mark.parametrize(
    "ignore_non_values, result",
    [
        (False, ["gold", False, "16 gb", None]),
        (True, ["gold", False, "16 gb"]),
    ],
)
def test_value_list(ignore_non_values, result):
    test_features_dict = {"color": "gold", "display": "retina"}
    test_specs_dict = {"proc": "i7", "ram": "16 gb"}

    value_list_parser = ed.ValueList(
        ed.Text(ed.jp("color")),
        ed.Bool(ed.jp("display"), contains=["retina2"]),
        ed.Text(ed.jp("ram"), source="specs"),
        ed.Text(ed.jp("features.brand")),
        ignore_non_values=ignore_non_values,
    )

    data_bag = DataBag(main=test_features_dict, specs=test_specs_dict)
    assert value_list_parser.parse(data_bag) == result
