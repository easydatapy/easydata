from easydata.queries import jp, key
from easydata.utils import parse
from tests.factory import load_data_bag_with_json

dict_db = load_data_bag_with_json("product")


def test_query_search():
    test_data = {"brand": "Groove"}

    assert parse.query_search(query=jp("brand"), data=test_data) == "Groove"


def test_query_search_data_bag():
    assert (
        parse.query_search(query=jp("prices.price"), data=dict_db, source="data")
        == 899.99
    )


def test_query_search_queries_list():
    assert (
        parse.query_search(
            query=[key("prices"), jp("price")], data=dict_db, source="data"
        )
        == 899.99
    )


def test_query_search_iter():
    test_data = {"brand": ["Groove", "Peach"]}

    assert parse.query_search_iter(query=jp("brand"), data=test_data) == [
        "Groove",
        "Peach",
    ]


def test_query_search_iter_data_bag():
    assert parse.query_search_iter(
        query=jp("prices").values(), data=dict_db, source="data"
    ) == [899.99, 799.99]
