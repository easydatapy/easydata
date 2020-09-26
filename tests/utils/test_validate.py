import pytest

from easydata.data import DataBag
from easydata.utils import validate


def test_key_in_item():
    # First test that it doesn't throw error if correct data is provided
    validate.key_in_item(item_key="title", item={"title": "EasyData Pro"})

    with pytest.raises(KeyError) as excinfo:
        validate.key_in_item(item_key="title", item={})

    assert "provided item key" in str(excinfo.value).lower()


def test_price_value_type():
    # First test that it doesn't throw error if correct data is provided
    validate.price_value_type(item_price_key="price", price="123")

    with pytest.raises(ValueError) as excinfo:
        validate.price_value_type(item_price_key="price", price=None)

    assert "price supported types are" in str(excinfo.value).lower()

    validate.price_value_type(item_price_key="price", price=None, allow_none=True)


def test_if_data_bag_with_source():
    validate.if_data_bag_with_source(DataBag(), "main")

    with pytest.raises(AttributeError) as excinfo:
        validate.if_data_bag_with_source(DataBag(), None)

    assert "data of type databag needs" in str(excinfo.value).lower()
