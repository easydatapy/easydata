import pytest

import easydata as ed
from easydata.data import DataBag
from easydata.utils import parse
from tests.factory import data_dict

dict_db = DataBag(main=data_dict.variants_data_multi)


@pytest.mark.parametrize(
    "test_data, query, result",
    [
        (
            {"brand": "Groove"},
            ed.jp("brand"),
            "Groove",
        ),
        (
            {"brand": "Groove"},
            ed.Text(
                ed.jp("brand"),
                uppercase=True,
            ),
            "GROOVE",
        ),
    ],
)
def test_query_search(test_data, query, result):
    assert parse.query_parser(query=query, data=test_data) == result


def test_query_search_data_bag():
    assert (
        parse.query_parser(query=ed.jp("data.title"), data=dict_db, source="main")
        == "EasyData Pro"
    )
