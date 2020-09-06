from easydata.queries import re
from tests import factory

db = factory.load_data_bag_with_html_text("product")


def test_re_query_get():
    assert re('"basePrice": "(.*?)",').get(db, "data") == "149.95"


def test_re_query_get_iter():
    expected_re_results = ["149.95", "0"]
    re_results = [i for i in re('"basePrice": "(.*?)",').get_iter(db, "data")]
    assert re_results == expected_re_results
