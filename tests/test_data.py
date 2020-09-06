from easydata.data import DataBag
from tests.factory import load_json
from tests.factory.parsers import SimpleJsonItemModel

jd = load_json("product")


def test_item_parser():
    data_bag = DataBag(None, data="groove")

    assert data_bag["data"] == "groove"

    data_bag.add("data_new", "peach")

    assert data_bag["data_new"] == "peach"


def test_data_bag_get():
    data_bag = DataBag(SimpleJsonItemModel(), data=jd)

    assert data_bag.get("name") == "Easybook Pro 13"

    # Test if results get cached
    assert data_bag.cached_results == {"name": "Easybook Pro 13"}

    data_bag_copy = data_bag.copy()

    # Test that data bag copy is cleared of cached results
    assert data_bag_copy.cached_results == {}


def test_data_bag_get_multi():
    data_bag = DataBag(SimpleJsonItemModel(), data=jd)

    req_params = ["brand", "currency", "name", "tags"]
    assert data_bag.get_multi(req_params) == {
        "brand": "Groove",
        "currency": "USD",
        "name": "Easybook Pro 13",
        "tags": ["phones", "ecommerce"],
    }

    # Test if multiple results gets cached
    assert all(k in data_bag.cached_results for k in req_params)


def test_data_bag_add():
    data_bag = DataBag(SimpleJsonItemModel(), data=jd)

    data_bag.add("brand_info", "Groove")

    assert data_bag["brand_info"] == "Groove"
