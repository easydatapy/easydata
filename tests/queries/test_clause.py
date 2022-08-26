import pytest

import easydata as ed
from easydata.exceptions import QuerySearchResultNotFound
from tests.factory import data_dict


@pytest.mark.parametrize(
    "queries, result",
    [
        (
            ed.cor(
                ed.jp("title2"),
                ed.jp("title"),
            ),
            "EasyBook pro 15",
        ),
        (
            ed.cor(
                ed.jp("color"),
                ed.jp("title"),
            ),
            "",
        ),
        (
            ed.cor(
                ed.jp(
                    "color",
                    empty_as_none=True,
                ),
                ed.jp("title"),
            ),
            "EasyBook pro 15",
        ),
        (
            ed.cor(
                ed.jp("multi"),
                ed.jp("title"),
            ),
            False,
        ),
        (
            ed.cor(
                ed.jp("title2"),
                ed.jp("title3"),
            ),
            None,
        ),
    ],
)
def test_cor(queries, result):
    assert queries.get(data_dict.item_with_options) == result


@pytest.mark.parametrize(
    "queries",
    [
        ed.cor(
            ed.jp_strict("title2"),
            ed.jp("title"),
        ),
        ed.cor(
            ed.jp("title2"),
            ed.jp_strict("title3"),
        ),
        ed.cor(
            ed.jp("title2"),
            ed.jp("title3", strict=True),
        ),
    ],
)
def test_cor_strict_query_non_existent_error(queries):
    with pytest.raises(QuerySearchResultNotFound):
        queries.get(data_dict.item_with_options)


@pytest.mark.parametrize(
    "queries, result",
    [
        (
            ed.cwith(
                ed.jp("brand"),
                ed.jp("name"),
            ),
            "EasyData",
        ),
        (
            ed.cwith(
                ed.jp("brand"),
                ed.jp("name2"),
            ),
            None,
        ),
        (
            ed.cwith(
                ed.jp("title"),
            ),
            "EasyBook pro 15",
        ),
        (
            ed.cwith(
                ed.jp("title"),
                ed.re("EasyBook (.*?) 15"),
            ),
            "pro",
        ),
        (
            ed.cwith(
                ed.jp("brand2"),
            ),
            None,
        ),
    ],
)
def test_cwith(queries, result):
    assert queries.get(data_dict.item_with_options) == result


@pytest.mark.parametrize(
    "queries",
    [
        ed.cwith(
            ed.jp("brand2"),
            ed.jp("name"),
        ),
    ],
)
def test_cwith_value_error(queries):
    with pytest.raises(ValueError):
        queries.get(data_dict.item_with_options)
