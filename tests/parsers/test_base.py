import pytest

from easydata.data import DataBag
from easydata.models import ItemModel
from easydata.parsers.data import Data
from easydata.queries import jp
from tests.factory import data_dict

db = DataBag(main=data_dict.item_with_options, additional_data=data_dict.stock)


def process_raw_value(value, data):
    return "{} {}".format(value, str(data["additional_data"]["stock"]))


def test_base_data_query():
    item_data = Data(query=jp("info.name"))
    assert item_data.parse(db) == "EasyBook pro 15"


def test_base_data_from_item():
    item_model = ItemModel()
    item_model.item_name = Data(query=jp("title"))
    item_model.item_brand = Data(from_item="name")

    result = item_model.parse_item(data_dict.title)
    assert result == {"brand": "Easybook Pro 13", "name": "Easybook Pro 13"}


def test_base_data_field_query_as_first_parameter():
    item_data = Data(jp("info.name"))
    assert item_data.parse(db) == "EasyBook pro 15"


@pytest.mark.parametrize(
    "query, default, test_data, result",
    [
        (jp("info.namewrong"), "Easybook Def 13", db, "Easybook Def 13"),
        (jp("info.name"), "Easybook Def 13", db, "EasyBook pro 15"),
    ],
)
def test_base_data_default(query, default, test_data, result):
    item_data = Data(query, default=default)
    assert item_data.parse(test_data) == result


def test_base_data_default_from_item():
    item_model = ItemModel()
    item_model.item_name = Data(query=jp("title"))
    item_model.item_brand = Data(query=jp("brandwrong"), default_from_item="name")

    result = item_model.parse_item(data_dict.title)
    assert result == {"brand": "Easybook Pro 13", "name": "Easybook Pro 13"}


@pytest.mark.parametrize(
    "query, source, test_data, result",
    [
        (jp("stock"), "additional_data", db, True),
        (None, "additional_data", db, {"stock": True}),
    ],
)
def test_base_data_field_different_source(query, source, test_data, result):
    item_data = Data(query, source=source)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "query, process_raw_value_callback, test_data, result",
    [
        (
            jp("info.name"),
            lambda value, data: value.replace("15", "13"),
            db,
            "EasyBook pro 13",
        ),
        (jp("info.name"), process_raw_value, db, "EasyBook pro 15 True"),
    ],
)
def test_base_data_field_process_raw_value(
    query, process_raw_value_callback, test_data, result
):

    item_data = Data(query, process_raw_value=process_raw_value_callback)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "query, process_value_callback, test_data, result",
    [
        (
            jp("info.name"),
            lambda value, data: "{} {}".format(
                value, str(data["additional_data"]["stock"])
            ),
            db,
            "EasyBook pro 15 True",
        ),
        (jp("info.name"), process_raw_value, db, "EasyBook pro 15 True"),
    ],
)
def test_base_data_field_process_value(
    query, process_value_callback, test_data, result
):

    item_data = Data(query, process_value=process_value_callback)
    assert item_data.parse(test_data) == result
