import pytest

from easydata import parsers
from easydata.exceptions import DropItem
from tests.factory import data_text


@pytest.mark.parametrize(
    "contains_keys, test_data, exception_msg",
    [
        (["pro 13"], data_text.title, ": easybook pro 13"),
        (["something", "pro 13"], data_text.title, ": easybook pro 13"),
    ],
)
def test_drop_contains(contains_keys, test_data, exception_msg):
    drop_contains_parser = parsers.DropContains(contains=contains_keys)

    with pytest.raises(DropItem) as excinfo:
        drop_contains_parser.parse(test_data)

    assert exception_msg in str(excinfo.value).lower()


@pytest.mark.parametrize(
    "ccontains_keys, test_data, exception_msg",
    [
        (["Pro 13"], data_text.title, ": easybook pro 13"),
        (["something", "Pro 13"], data_text.title, ": easybook pro 13"),
    ],
)
def test_drop_contains_case(ccontains_keys, test_data, exception_msg):
    drop_contains_parser = parsers.DropContains(ccontains=ccontains_keys)

    with pytest.raises(DropItem) as excinfo:
        drop_contains_parser.parse(test_data)

    assert exception_msg in str(excinfo.value).lower()


@pytest.mark.parametrize(
    "test_data, exception_msg",
    [
        ("", "Name cannot be empty"),
        (None, "Name is empty!"),
        ([], "No links extracted!"),
        ({}, "No info data!"),
        (False, "Out of stock!"),
    ],
)
def test_drop_empty(test_data, exception_msg):
    drop_parser = parsers.DropEmpty(error_msg=exception_msg)

    with pytest.raises(DropItem) as excinfo:
        drop_parser.parse(test_data)

    assert exception_msg in str(excinfo.value)
