import json

from easydata.data import DataBag
from easydata.managers import ModelManager
from tests.factory import data_dict
from tests.factory.models import ProductJsonModel


def load_data_bag_with_model():
    model_manager = ModelManager(ProductJsonModel())

    data_bag = DataBag(main=json.dumps(data_dict.item_with_options))
    data_bag.init_model_manager(model_manager)
    return data_bag


def test_item_parser():
    data_bag = DataBag(main="groove")

    assert data_bag["main"] == "groove"

    data_bag.add("main_new", "peach")

    assert data_bag["main_new"] == "peach"


def test_data_bag_get():
    data_bag = load_data_bag_with_model()

    assert data_bag.get("name") == "EasyBook pro 15"

    # Test if results get cached
    assert data_bag.cached_results == {"name": "EasyBook pro 15"}

    data_bag_copy = data_bag.copy()

    # Test that data bag copy is cleared of cached results
    assert data_bag_copy.cached_results == {}


def test_data_bag_get_multi():
    data_bag = load_data_bag_with_model()

    req_params = ["currency", "name", "price", "sale_price", "tags"]

    assert data_bag.get_multi(req_params) == {
        "currency": "USD",
        "name": "EasyBook pro 15",
        "price": 99.99,
        "sale_price": 49.99,
        "tags": ["notebook", "ecommerce"],
    }

    # Test if multiple results gets cached
    assert all(k in data_bag.cached_results for k in req_params)


def test_data_bag_add():
    data_bag = load_data_bag_with_model()

    data_bag.add("brand_info", "Groove")

    assert data_bag["brand_info"] == "Groove"
