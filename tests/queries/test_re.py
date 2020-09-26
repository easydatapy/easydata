import json

import pytest
from pyquery import PyQuery

from easydata.data import DataBag
from easydata.queries import re

json_text = """
let spConfig = {
    "basePrice": "149.95",
    "prices": {
        "basePrice": "0"
    }
};
"""

html_text = "<div><p>EasyData</p></div>"


@pytest.mark.parametrize(
    "query, test_data, source, result",
    [
        ('basePrice": "(.*?)"', json_text, "main", "149.95"),
        ('basePrice": "(.*?)"', json_text, None, "149.95"),
        ('wrongSearch": "(.*?)"', json_text, None, None),
        ('basePrice": "(.*?)"', None, None, None),
        ('basePrice": "(.*?)"', "", None, None),
        ('basePrice": "(.*?)"', DataBag(main=json_text), "main", "149.95"),
        ('brand": "(.*?)"', {"brand": "EasyData"}, None, "EasyData"),
        ("<p>(.*?)</p>", PyQuery("<div><p>EasyData</p></div>"), None, "EasyData"),
        # Test that outer html tags are also shown when PyQuery converts back to text
        ("<p>(.*?)</p>", PyQuery("<p>EasyData</p>"), None, "EasyData"),
    ],
)
def test_re_query(query, test_data, source, result):
    assert re(query).get(test_data, source) == result


def test_re_query_wrong_type_exception():
    with pytest.raises(TypeError) as excinfo:
        re('basePrice": "(.*?)"').get(json)

    assert "provided data" in str(excinfo.value).lower()


def test_re_query_ignore_case():
    re_query = re(
        query='"baseprice": "(.*?)"',
        ignore_case=True,
    )
    assert re_query.get(json_text, "main") == "149.95"


@pytest.mark.parametrize(
    "query, dotall, ignore_case, result",
    [
        ("spConfig = (.*?);", True, False, "149.95"),
        ("spConfig = (.*?);", False, False, None),
        ("spconfig = (.*?);", True, True, "149.95"),
    ],
)
def test_re_query_dotall_ignore_case(query, dotall, ignore_case, result):
    re_query = re(query=query, dotall=dotall, ignore_case=ignore_case)

    json_result = re_query.get(json_text, "main")

    if json_result:
        json_data = json.loads(json_result)
        assert json_data["basePrice"] == result
    else:
        assert json_result == result


def test_re_query_multiline_ignore_case():
    json_result_text = re("spConfig = (.*?);").get(json_text, "main")
    json_data = json.loads(json_result_text)

    assert json_data["basePrice"] == "149.95"


def test_re_query_get_list():
    assert re('"basePrice": "(.*?)"::all').get(json_text, "main") == ["149.95", "0"]


def test_re_query_missing_pattern_with_pseudo_key_all_exception():
    with pytest.raises(ValueError) as excinfo:
        re("::all").get(json_text, "main")

    assert "regex pattern is required beside ::all" in str(excinfo.value).lower()
