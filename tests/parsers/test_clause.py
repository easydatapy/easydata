import pytest

from easydata import parsers
from easydata.data import DataBag
from easydata.queries import jp, pq
from tests.factory import data_html


def test_union():
    test_html = """
        <p class="brand">EasyData</p>
    """

    union_parser = parsers.Union(
        parsers.Text(pq(".brand-wrong::text")),
        parsers.Text(pq(".brand::text")),
    )
    assert union_parser.parse(test_html) == "EasyData"


def test_union_first():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    union_parser = parsers.Union(
        parsers.Text(pq(".brand::text")),
        parsers.Text(pq("#name::text")),
    )
    assert union_parser.parse(test_html) == "EasyData"


def test_union_none():
    test_html = """
        <p class="brand">EasyData</p>
    """

    union_parser = parsers.Union(
        parsers.Text(pq(".brand-wrong::text")),
        parsers.Text(pq(".brand-wrong-again::text")),
    )
    assert union_parser.parse(test_html) is None


def test_with():
    with_parser = parsers.With(
        parsers.Sentences(pq("#description .features::text"), allow=["date added"]),
        parsers.DateTimeSearch(),
    )
    assert with_parser.parse(data_html.features) == "12/12/2018 10:55:00"

    with_parser = parsers.With(
        parsers.Sentences(pq("#description .features::text"), allow=["date added"]),
        parsers.Text(split_key=("added:", -1)),
        parsers.DateTime(),
    )
    assert with_parser.parse(data_html.features) == "12/12/2018 10:55:00"


def test_join_text():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    join_text_parser = parsers.ConcatText(
        parsers.Text(pq(".brand::text")), parsers.Text(pq("#name::text"))
    )
    assert join_text_parser.parse(test_html) == "EasyData Easybook Pro 13"

    join_text_parser = parsers.ConcatText(
        parsers.Text(pq(".brand-wrong-selector::text")), parsers.Text(pq("#name::text"))
    )
    assert join_text_parser.parse(test_html) == "Easybook Pro 13"


def test_join_text_custom_separator():
    test_html = """
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    """

    join_text_parser = parsers.ConcatText(
        parsers.Text(pq(".brand::text")), parsers.Text(pq("#name::text")), separator="-"
    )
    assert join_text_parser.parse(test_html) == "EasyData-Easybook Pro 13"


def test_join_list():
    test_dict = {"features": ["gold color", "retina"], "specs": ["i7 proc", "16 gb"]}

    join_list_parser = parsers.JoinList(
        parsers.List(jp("features"), parser=parsers.Text()),
        parsers.List(jp("specs"), parser=parsers.Text()),
    )

    expected_result = ["gold color", "retina", "i7 proc", "16 gb"]
    assert join_list_parser.parse(test_dict) == expected_result


def test_join_dict():
    test_dict = {
        "features": {"color": "gold", "display": "retina"},
        "specs": {"proc": "i7", "ram": "16 gb"},
    }

    join_dict_parser = parsers.MergeDict(
        parsers.Dict(
            jp("features"), key_parser=parsers.Text(), val_parser=parsers.Text()
        ),
        parsers.Dict(jp("specs"), key_parser=parsers.Text(), val_parser=parsers.Text()),
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

    item_dict_parser = parsers.ItemDict(
        ignore_non_values=ignore_non_values,
        color=parsers.Text(jp("color")),
        ram=parsers.Text(jp("ram"), source="specs"),
        brand=parsers.Text(jp("features.brand")),
    )

    data_bag = DataBag(main=test_features_dict, specs=test_specs_dict)
    assert item_dict_parser.parse(data_bag) == result


@pytest.mark.parametrize(
    "ignore_non_values, result",
    [
        (False, ["gold", False, "16 gb", None]),
        (True, ["gold", False, "16 gb"]),
    ],
)
def test_item_list(ignore_non_values, result):
    test_features_dict = {"color": "gold", "display": "retina"}
    test_specs_dict = {"proc": "i7", "ram": "16 gb"}

    item_list_parser = parsers.ItemList(
        parsers.Text(jp("color")),
        parsers.Bool(jp("display"), contains=["retina2"]),
        parsers.Text(jp("ram"), source="specs"),
        parsers.Text(jp("features.brand")),
        ignore_non_values=ignore_non_values,
    )

    data_bag = DataBag(main=test_features_dict, specs=test_specs_dict)
    assert item_list_parser.parse(data_bag) == result
