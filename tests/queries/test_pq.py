import pytest

from easydata.queries import pq
from tests.factory import data_html

exp_result_images = [
    "http://demo.com/img1.jpg",
    "http://demo.com/img2.jpg",
    "http://demo.com/img3.jpg",
]


def test_pq_query_text():
    assert pq(".brand::text").get(data_html.item_with_breadcrumbs) == "EasyData"


@pytest.mark.parametrize(
    "query, result",
    [
        (".breadcrumbs .breadcrumb::text", "Home"),
        (".breadcrumbs .breadcrumb::text-all", "Home Phone Smartphone"),
    ],
)
def test_pq_query_all(query, result):
    assert pq(query).get(data_html.item_with_breadcrumbs) == result

    assert pq(query=query).get(data_html.item_with_breadcrumbs) == result


@pytest.mark.parametrize(
    "query",
    [".images img::attr(src)-items", ".images img::src-items"],
)
def test_pq_query_items(query):
    assert pq(query).get(data_html.item_with_breadcrumbs) == exp_result_images


def test_pq_query_attr():
    exp_result = "smartphone"
    test_data = data_html.item_with_breadcrumbs
    assert pq('[name="category"]::attr(value)').get(test_data) == exp_result


def test_pq_query_attr_all():
    test_all_html = '<input some-strange-value="EasyData">'
    assert pq("input::attr(some-strange-value)-all").get(test_all_html) == "EasyData"


def test_pq_query_attr_val():
    result = pq('[name="category"]::val').get(data_html.item_with_breadcrumbs)
    assert result == "smartphone"


def test_pq_query_attr_name():
    result = pq('[name="category"]::name').get(data_html.item_with_breadcrumbs)
    assert result == "category"


def test_pq_query_attr_content():
    result = pq('[name="category"]::content').get(data_html.item_with_breadcrumbs)
    assert result == "phone"


def test_pq_query_attr_src():
    result = pq(".images img::src").get(data_html.item_with_breadcrumbs)
    assert result == "http://demo.com/img1.jpg"


def test_pq_query_attr_href():
    result = pq("#url::href").get(data_html.item_with_breadcrumbs)
    assert result == "http://demo.com/product/123"


def test_pq_query_remove_query():
    exp_result = "Test Product Item"
    test_data = data_html.item_with_breadcrumbs
    assert pq(".name::text", remove_query=".brand").get(test_data) == exp_result


def test_pq_query_html():
    exp_result = '<div class="brand">EasyData</div>\nTest Product Item'
    test_data = data_html.item_with_breadcrumbs
    assert pq(".name::html").get(test_data).strip().replace("  ", "") == exp_result
