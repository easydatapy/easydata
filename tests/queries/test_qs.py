import pytest

import easydata as ed
from tests.factory import data_dict


@pytest.mark.parametrize(
    "queries, result",
    [
        (
            ed.qs(
                ed.jp("title2"),
                ed.jp("title"),
            ),
            "EasyBook pro 15",
        ),
        (
            ed.qs(
                ed.jp("color"),
                ed.jp("title"),
            ),
            "",
        ),
        (
            ed.qs(
                ed.jp(
                    "color",
                    empty_as_none=True,
                ),
                ed.jp("title"),
            ),
            "EasyBook pro 15",
        ),
        (
            ed.qs(
                ed.jp("multi"),
                ed.jp("title"),
            ),
            False,
        ),
    ],
)
def test_qs(queries, result):
    assert queries.get(data_dict.item_with_options) == result
