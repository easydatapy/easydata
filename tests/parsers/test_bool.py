import pytest

from easydata import parsers
from easydata.queries import key, pq
from tests.factory import data_dict, data_text


@pytest.mark.parametrize(
    "query, test_data, result",
    [
        (key("stock"), data_dict.stock, True),
        (key("stock2"), data_dict.stock, False),
    ],
)
def test_bool(query, test_data, result):
    bool_parser = parsers.Bool(query)
    assert bool_parser.parse(test_data) is result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (123, True),
        (123.45, True),
        (0.15, True),
        (-0.15, True),
        (0, False),
        ("True", True),
        ("False", False),
        ("true", True),
        ("false", False),
    ],
)
def test_bool_various_types(test_data, result):
    assert parsers.Bool().parse(test_data) is result


@pytest.mark.parametrize(
    "contains_keys, test_data, result",
    [
        (["pro 13"], data_text.title, True),
        (["something", "pro 13"], data_text.title, True),
        (["pros 13"], data_text.title, False),
    ],
)
def test_bool_contains(contains_keys, test_data, result):
    bool_parser = parsers.Bool(contains=contains_keys)
    assert bool_parser.parse(test_data) is result


@pytest.mark.parametrize(
    "ccontains_keys, test_data, result",
    [
        (["Pro 13"], data_text.title, True),
        (["something", "Pro 13"], data_text.title, True),
        (["pro 13"], data_text.title, False),
    ],
)
def test_bool_contains_case(ccontains_keys, test_data, result):
    bool_parser = parsers.Bool(ccontains=ccontains_keys)
    assert bool_parser.parse(test_data) is result


@pytest.mark.parametrize(
    "query, contains_query, test_data, result",
    [
        (pq("#full-name::text"), pq(".brand::text"), "Easybook Pro 13", False),
        (pq("#full-name::text"), pq(".brand::text-items"), "Easybook Pro 13", False),
    ],
)
def test_bool_contains_query(query, contains_query, test_data, result):
    bool_parser = parsers.Bool(query, contains_query=contains_query)
    assert bool_parser.parse(test_data) is result
