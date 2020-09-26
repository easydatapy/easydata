import pytest

from easydata.data import DataBag
from easydata.queries import key

test_data_dict = {"product_type": "smartphone"}

test_data_json = '{"product_type": "smartphone"}'

test_data_prices_dict = {"prices": {"price": 79, "sale_price": 50}}

test_data_images_dict = {
    "image_list": [
        "https://demo.com/imgs/1-zoom.jpg",
        "https://demo.com/imgs/2-zoom.jpg",
    ]
}

expected_image_list = [
    "https://demo.com/imgs/1-zoom.jpg",
    "https://demo.com/imgs/2-zoom.jpg",
]


@pytest.mark.parametrize(
    "query, test_data, result",
    [
        ("product_type", test_data_dict, "smartphone"),
        ("", test_data_dict, {"product_type": "smartphone"}),
        ("::yaml", test_data_dict, "product_type: smartphone\n"),
        ("::json", test_data_dict, '{"product_type": "smartphone"}'),
        ("::str", test_data_dict, "{'product_type': 'smartphone'}"),
        ("prices::values", test_data_prices_dict, [79, 50]),
        ("prices::keys", test_data_prices_dict, ["price", "sale_price"]),
        ("prices::values-yaml", test_data_prices_dict, "- 79\n- 50\n"),
        ("prices::values-json", test_data_prices_dict, "[79, 50]"),
        ("prices::values-str", test_data_prices_dict, "[79, 50]"),
        ("prices::keys-yaml", test_data_prices_dict, "- price\n- sale_price\n"),
        ("prices::keys-json", test_data_prices_dict, '["price", "sale_price"]'),
        ("prices::keys-str", test_data_prices_dict, "['price', 'sale_price']"),
        ("product_type", test_data_json, "smartphone"),
        ("product_type", None, None),
        ("product_type", "", None),
    ],
)
def test_key_query(query, test_data, result):
    assert key(query).get(test_data) == result


@pytest.mark.parametrize(
    "query, test_data, result",
    [
        ("product_type", test_data_dict, "smartphone"),
        ("product_type", test_data_json, "smartphone"),
    ],
)
def test_key_query_get_data_bag(query, test_data, result):
    db = DataBag(main=test_data)
    assert key(query).get(db) == result


@pytest.mark.parametrize(
    "query, test_data",
    [
        ("product_type", None),
        ("product_type", ""),
    ],
)
def test_key_query_get_data_bag_bad_source(query, test_data):
    db = DataBag(main=test_data)

    with pytest.raises(ValueError) as excinfo:
        key(query).get(db)

    assert "provided data from source" in str(excinfo.value).lower()


def test_key_query_get_data_bag_source():
    db = DataBag(json_data=test_data_dict)

    assert key("product_type").get(db, source="json_data") == "smartphone"
    assert key("product_type").get(db, "json_data") == "smartphone"


@pytest.mark.parametrize(
    "query, test_data, result",
    [
        ("image_list", test_data_images_dict, expected_image_list),
        (None, expected_image_list, expected_image_list),
    ],
)
def test_key_query_get_list(query, test_data, result):
    assert key(query).get(test_data) == result


def test_key_query_pseudo_key_exception():
    with pytest.raises(ValueError) as excinfo:
        key("prices::wrong").get(test_data_prices_dict)

    assert "pseudo key 'wrong' is not supported" in str(excinfo.value).lower()
