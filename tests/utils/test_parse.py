from easydata.data import DataBag
from easydata.queries import jp
from easydata.utils import parse
from tests.factory import data_dict

dict_db = DataBag(main=data_dict.variants_data_multi)


def test_query_search():
    test_data = {"brand": "Groove"}

    assert parse.query_search(query=jp("brand"), data=test_data) == "Groove"


def test_query_search_data_bag():
    assert (
        parse.query_search(query=jp("data.title"), data=dict_db, source="main")
        == "EasyData Pro"
    )
