import pytest

import easydata as ed
from easydata.exceptions import QuerySearchDataEmpty, QuerySearchResultNotFound
from tests.factory import data_dict


@pytest.mark.parametrize(
    "query, result",
    [
        ("title", "EasyBook pro 15"),
        ("brand.name", "EasyData"),
        ("brand::values", ["EasyData", "Slovenia"]),
        ("brand::keys", ["name", "origin"]),
        ("brand::values", ["EasyData", "Slovenia"]),
        ("brand::keys", ["name", "origin"]),
        ("brand::values-json", '["EasyData", "Slovenia"]'),
        ("brand::keys-yaml", "- name\n- origin\n"),
        ("brand::values-str", "['EasyData', 'Slovenia']"),
        (
            "images[]",
            [
                "https://demo.com/img1.jpg",
                "https://demo.com/img2.jpg",
                "https://demo.com/img3.jpg",
            ],
        ),
        ("images[0:2]", ["https://demo.com/img1.jpg", "https://demo.com/img2.jpg"]),
        ("images[:2]", ["https://demo.com/img1.jpg", "https://demo.com/img2.jpg"]),
        ("images[1:]", ["https://demo.com/img2.jpg", "https://demo.com/img3.jpg"]),
        ("images[:2]", ["https://demo.com/img1.jpg", "https://demo.com/img2.jpg"]),
        ("images[1]", "https://demo.com/img2.jpg"),
        (
            "image_data[].zoom",
            ["https://demo.com/img1.jpg", "https://demo.com/img2.jpg"],
        ),
        ("image_data[0].zoom", "https://demo.com/img1.jpg"),
        (
            "options[].{name: name, stock: availability.value}",
            [{"name": "Monitor", "stock": "yes"}, {"name": "Mouse", "stock": "no"}],
        ),
        (
            "options[].{name: name, stock: availability.value}",
            [{"name": "Monitor", "stock": "yes"}, {"name": "Mouse", "stock": "no"}],
        ),
        (
            "options[].{name: name, stock: availability.value}::dict(name:stock)",
            {"Monitor": "yes", "Mouse": "no"},
        ),
        ("options[?contains(name, 'Monitor')].availability.value", ["yes"]),
        ("brand::json", '{"name": "EasyData", "origin": "Slovenia"}'),
        ("brand::yaml", "name: EasyData\norigin: Slovenia\n"),
        (
            "images::json",
            (
                (
                    '["https://demo.com/img1.jpg", '
                    '"https://demo.com/img2.jpg", '
                    '"https://demo.com/img3.jpg"]'
                )
            ),
        ),
        ("color", ""),
        ("multi", False),
        ("in_stock", True),
    ],
)
def test_jp_query(query, result):
    assert ed.jp(query).get(data_dict.item_with_options) == result


def test_jp_query_add_query_prefix():
    jp_query = ed.jp("name")

    jp_query.add_query_prefix("brand.")

    assert jp_query.get(data_dict.item_with_options) == "EasyData"


@pytest.mark.parametrize(
    "query, result",
    [
        ("title", "EasyBook pro 15"),
        ("color", ""),
        ("multi", False),
        ("in_stock", True),
    ],
)
def test_jp_query_strict(query, result):
    assert ed.jp_strict(query).get(data_dict.item_with_options) == result


@pytest.mark.parametrize(
    "query, params, result",
    [
        (
            "brand.{name}",
            {"name": ed.Data(ed.jp("name_key"))},
            "EasyData",
        ),
        (
            "options[].{{name: {name}, stock: availability.value}}",
            {"name": ed.Data(ed.jp("name_key"))},
            [{"name": "Monitor", "stock": "yes"}, {"name": "Mouse", "stock": "no"}],
        ),
        (
            "options[?contains(name, '{value}')].availability.value",
            {"value": ed.Data(ed.jp("option_name_contains"))},
            ["yes"],
        ),
        ("brand.{name}", {"name": ed.Data(ed.jp("name_key_non"))}, None),
        ("brand.name", {"name": ed.Data(ed.jp("name_key"))}, "EasyData"),
        ("brand.name", {}, "EasyData"),
        ("brand.name", None, "EasyData"),
    ],
)
def test_jp_query_params(query, params, result):
    assert ed.jp(query, params=params).get(data_dict.item_with_options) == result


@pytest.mark.parametrize(
    "query, test_data, result",
    [
        ("", {"name": "EasyData"}, {"name": "EasyData"}),
        ("::json", {"name": "EasyData"}, '{"name": "EasyData"}'),
        ("::yaml", {"name": "EasyData"}, "name: EasyData\n"),
        ("::str", {"name": "EasyData"}, "{'name': 'EasyData'}"),
        ("", "", None),
        ("::yaml", "", None),
        ("::json", "", None),
        ("::str", "", None),
        ("::values", "", None),
        ("::keys", "", None),
    ],
)
def test_jp_query_empty_selector(query, test_data, result):
    assert ed.jp(query).get(test_data) == result


def test_jp_query_strict_query_non_existent_error():
    with pytest.raises(QuerySearchResultNotFound):
        assert ed.jp_strict("title2").get(data_dict.item_with_options)


def test_jp_query_strict_data_empty_error():
    with pytest.raises(QuerySearchDataEmpty):
        assert ed.jp_strict("title").get(None)
