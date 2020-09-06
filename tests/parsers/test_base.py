import pytest

from easydata.parsers.data import Data
from easydata.queries import jp, key
from tests.factory import load_data_bag_with_json

db = load_data_bag_with_json("product")
db["additional_data"] = {"proc": "i7"}


def process_raw_value(value, data):
    return "{} {}".format(value, data["additional_data"]["proc"])


def test_base_data_field_query():
    item_data = Data(query=jp("info.name"))
    assert item_data.parse(db) == "Easybook Pro 13"


def test_base_data_field_query_as_first_parameter():
    item_data = Data(jp("info.name"))
    assert item_data.parse(db) == "Easybook Pro 13"


@pytest.mark.parametrize(
    "query, query2, test_data, result",
    [
        (jp("info"), key("name"), db, "Easybook Pro 13"),
        # Test that None is returned if first query in list returns None
        (jp("infowrong"), key("name"), db, None),
        # Test that None is returned if last query in list returns None
        (jp("info"), key("namewrong"), db, None),
    ],
)
def test_base_data_field_query_chain(query, query2, test_data, result):
    item_data = Data([query, query2])
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "query, default, test_data, result",
    [
        (jp("info.namewrong"), "Easybook Def 13", db, "Easybook Def 13"),
        (jp("info.name"), "Easybook Def 13", db, "Easybook Pro 13"),
    ],
)
def test_base_data_field_query_default(query, default, test_data, result):
    item_data = Data(query, default=default)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "query, source, test_data, result",
    [
        (jp("proc"), "additional_data", db, "i7"),
        (None, "additional_data", db, {"proc": "i7"}),
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
            lambda value, data: value.replace("13", "15"),
            db,
            "Easybook Pro 15",
        ),
        (jp("info.name"), process_raw_value, db, "Easybook Pro 13 i7"),
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
            lambda value, data: "{} {}".format(value, data["additional_data"]["proc"]),
            db,
            "Easybook Pro 13 i7",
        ),
        (jp("info.name"), process_raw_value, db, "Easybook Pro 13 i7"),
    ],
)
def test_base_data_field_process_value(
    query, process_value_callback, test_data, result
):

    item_data = Data(query, process_value=process_value_callback)
    assert item_data.parse(test_data) == result
