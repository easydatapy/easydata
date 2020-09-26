import pytest

from easydata.queries import jp
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
    ],
)
def test_jp_query(query, result):
    assert jp(query).get(data_dict.item_with_options) == result


@pytest.mark.parametrize(
    "query, params, result",
    [
        ("brand.{name}", {"name": "name"}, "EasyData"),
        (
            "options[].{{name: {name}, stock: availability.value}}",
            {"name": "name"},
            [{"name": "Monitor", "stock": "yes"}, {"name": "Mouse", "stock": "no"}],
        ),
        (
            "options[?contains(name, '{value}')].availability.value",
            {"value": "Moni"},
            ["yes"],
        ),
        ("brand.{name}", {"name": None}, None),
        ("brand.name", {"name": "name"}, "EasyData"),
        ("brand.name", {}, "EasyData"),
        ("brand.name", None, "EasyData"),
    ],
)
def test_jp_query_params(query, params, result):
    assert jp(query).get(data_dict.item_with_options, query_params=params) == result


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
    assert jp(query).get(test_data) == result
