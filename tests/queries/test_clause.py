import pytest

import easydata as ed
from tests.factory import data_dict


@pytest.mark.parametrize(
    "queries, result",
    [
        (
            ed.orc(
                ed.jp("title2"),
                ed.jp("title"),
            ),
            "EasyBook pro 15",
        ),
        (
            ed.orc(
                ed.jp("color"),
                ed.jp("title"),
            ),
            "",
        ),
        (
            ed.orc(
                ed.jp(
                    "color",
                    empty_as_none=True,
                ),
                ed.jp("title"),
            ),
            "EasyBook pro 15",
        ),
        (
            ed.orc(
                ed.jp("multi"),
                ed.jp("title"),
            ),
            False,
        ),
    ],
)
def test_orc(queries, result):
    assert queries.get(data_dict.item_with_options) == result
