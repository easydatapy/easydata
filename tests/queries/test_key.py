from easydata.queries import key
from tests import factory

jd = factory.load_data_bag_with_json("product")

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


def test_key_query_get():
    assert key("product_type").get(jd, "data") == "smartphone"

    test_data_dict = {"product_type": "smartphone"}
    assert key("product_type").get(test_data_dict) == "smartphone"


def test_key_query_get_keys():
    result = key("prices").keys().get(test_data_prices_dict)
    assert result == ["price", "sale_price"]


def test_key_query_get_values():
    result = key("prices").values().get(test_data_prices_dict)
    assert result == [79, 50]


def test_key_query_get_iter():
    result = key("image_list").get_iter(jd, "data")
    assert list(result) == expected_image_list

    result = key("image_list").get_iter(test_data_images_dict)
    assert list(result) == expected_image_list


def test_key_query_get_iter_keys():
    result = key("prices").keys().get_iter(test_data_prices_dict)
    assert list(result) == ["price", "sale_price"]


def test_key_query_get_iter_values():
    result = key("prices").values().get_iter(test_data_prices_dict)
    assert list(result) == [79, 50]
