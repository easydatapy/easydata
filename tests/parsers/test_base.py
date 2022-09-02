import pytest

import easydata as ed
from easydata.data import DataBag
from tests.factory import data_dict

db = DataBag(main=data_dict.item_with_options, additional_data=data_dict.stock)


def process_raw_value(value, data):
    return "{} {}".format(value, str(data["additional_data"]["stock"]))


def test_base_data_query():
    item_data = ed.Data(query=ed.jp("info.name"))
    assert item_data.parse(db) == "EasyBook pro 15"


def test_base_data_add_query():
    item_data = ed.Data()

    item_data.add_query(ed.jp("info.name"))

    assert item_data.parse(db) == "EasyBook pro 15"


def test_base_data_add_source():
    item_data = ed.Data()

    # Check default source name
    assert item_data.source == "main"

    # Add new source name
    item_data.add_source("country")

    assert item_data.source == "country"


def test_base_data_from_item():
    item_model = ed.ItemModel()
    item_model.item_name = ed.Data(query=ed.jp("title"))
    item_model.item_brand = ed.Data(from_item="name")

    result = item_model.parse_item(data_dict.title)
    assert result == {"brand": "Easybook Pro 13", "name": "Easybook Pro 13"}


def test_base_data_field_query_as_first_parameter():
    item_data = ed.Data(ed.jp("info.name"))
    assert item_data.parse(db) == "EasyBook pro 15"


@pytest.mark.parametrize(
    "query, default, test_data, result",
    [
        (ed.jp("info.namewrong"), "Easybook Def 13", db, "Easybook Def 13"),
        (ed.jp("info.name"), "Easybook Def 13", db, "EasyBook pro 15"),
    ],
)
def test_base_data_default(query, default, test_data, result):
    item_data = ed.Data(query, default=default)
    assert item_data.parse(test_data) == result


def test_base_data_default_from_item():
    item_model = ed.ItemModel()
    item_model.item_name = ed.Data(query=ed.jp("title"))
    item_model.item_brand = ed.Data(query=ed.jp("brandwrong"), default_from_item="name")

    result = item_model.parse_item(data_dict.title)
    assert result == {"brand": "Easybook Pro 13", "name": "Easybook Pro 13"}


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.Data(), [], []),
        (ed.Data(), {}, {}),
        (ed.Data(), False, False),
        (ed.Data(), "", ""),
        (ed.Data(), None, None),
        (ed.Data(empty_as_none=True), [], None),
        (ed.Data(empty_as_none=True), {}, None),
        # Boolean false is not considered as empty
        (ed.Data(empty_as_none=True), False, False),
        (ed.Data(empty_as_none=True), "", None),
    ],
)
def test_base_data_empty_as_none(parser, test_data, result):
    assert parser.parse(test_data) == result


@pytest.mark.parametrize(
    "query, source, test_data, result",
    [
        (ed.jp("stock"), "additional_data", db, True),
        (None, "additional_data", db, {"stock": True}),
    ],
)
def test_base_data_field_different_source(query, source, test_data, result):
    item_data = ed.Data(query, source=source)
    assert item_data.parse(test_data) == result


def test_base_data_with_query_source():
    item_data = ed.Data(query=ed.jp("stock", source="additional_data"))
    assert item_data.parse(db) is True


@pytest.mark.parametrize(
    "query, process_raw_value_callback, test_data, result",
    [
        (
            ed.jp("info.name"),
            lambda value, data: value.replace("15", "13"),
            db,
            "EasyBook pro 13",
        ),
        (
            ed.jp("info.name"),
            ed.Text(replace_keys=[("15", "13")]),
            db,
            "EasyBook pro 13",
        ),
        (ed.jp("info.name"), process_raw_value, db, "EasyBook pro 15 True"),
    ],
)
def test_base_data_field_process_raw_value(
    query, process_raw_value_callback, test_data, result
):

    item_data = ed.Data(query, process_raw_value=process_raw_value_callback)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "query, process_value_callback, test_data, result",
    [
        (
            ed.jp("info.name"),
            lambda value, data: "{} {}".format(
                value, str(data["additional_data"]["stock"])
            ),
            db,
            "EasyBook pro 15 True",
        ),
        (
            None,
            ed.Text(remove_keys=["'"], split_keys=[("Easy", -1), "pro"]),
            "EasyBook' pro 15",
            "Book",
        ),
        (ed.jp("info.name"), process_raw_value, db, "EasyBook pro 15 True"),
    ],
)
def test_base_data_field_process_value(
    query, process_value_callback, test_data, result
):

    item_data = ed.Data(query, process_value=process_value_callback)
    assert item_data.parse(test_data) == result
