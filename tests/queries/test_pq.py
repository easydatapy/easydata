import pytest

import easydata as ed
from easydata.exceptions import QuerySearchDataEmpty, QuerySearchResultNotFound
from tests.factory import data_html

exp_result_images = [
    "https://demo.com/img1.jpg",
    "https://demo.com/img2.jpg",
    "https://demo.com/img3.jpg",
]


@pytest.mark.parametrize(
    "query, test_html, result",
    [
        ('[itemprop="name"]::text', data_html.prices_and_variants, "EasyBook Pro 15"),
        (".name .brand::text", data_html.item_with_breadcrumbs, "EasyData"),
    ],
)
def test_pq_text(query, test_html, result):
    assert ed.pq(query).get(test_html) == result


@pytest.mark.parametrize(
    "query, result",
    [
        (".breadcrumbs .breadcrumb::text", "Home"),
        (".breadcrumbs .breadcrumb::text-all", "Home Phone Smartphone"),
    ],
)
def test_pq_all(query, result):
    assert ed.pq(query).get(data_html.item_with_breadcrumbs) == result

    assert ed.pq(query=query).get(data_html.item_with_breadcrumbs) == result


@pytest.mark.parametrize(
    "query",
    [".images img::attr(src)-items", ".images img::src-items"],
)
def test_pq_items(query):
    assert ed.pq(query).get(data_html.item_with_breadcrumbs) == exp_result_images


def test_pq_attr():
    exp_result = "smartphone"
    test_data = data_html.item_with_breadcrumbs
    assert ed.pq('[name="category"]::attr(value)').get(test_data) == exp_result


def test_pq_attr_all():
    test_all_html = '<input some-strange-value="EasyData">'
    assert ed.pq("input::attr(some-strange-value)-all").get(test_all_html) == "EasyData"


def test_pq_attr_val():
    result = ed.pq('[name="category"]::val').get(data_html.item_with_breadcrumbs)
    assert result == "smartphone"


def test_pq_attr_name():
    result = ed.pq('[name="category"]::name').get(data_html.item_with_breadcrumbs)
    assert result == "category"


def test_pq_attr_class():
    result = ed.pq(".availability::class").get(data_html.prices_and_variants)
    assert result == "instock availability"


def test_pq_attr_content():
    result = ed.pq('[name="category"]::content').get(data_html.item_with_breadcrumbs)
    assert result == "phone"


def test_pq_attr_src():
    result = ed.pq(".images img::src").get(data_html.item_with_breadcrumbs)
    assert result == "https://demo.com/img1.jpg"


def test_pq_attr_href():
    result = ed.pq("#url::href").get(data_html.item_with_breadcrumbs)
    assert result == "https://demo.com/product/123"


def test_pq_remove_query():
    exp_result = "Test Product Item"
    test_data = data_html.item_with_breadcrumbs
    assert ed.pq(".name::text", remove_query=".brand").get(test_data) == exp_result


def test_pq_html():
    exp_result = '<div class="brand">EasyData</div>\nTest Product Item'
    test_data = data_html.item_with_breadcrumbs
    assert ed.pq(".name::html").get(test_data).strip().replace("  ", "") == exp_result


@pytest.mark.parametrize(
    "query, test_html, result",
    [
        (
            ".availability::has_class(instock)",
            data_html.prices_and_variants,
            True,
        ),
        (
            ".availability::has_class(outofstock)",
            data_html.prices_and_variants,
            False,
        ),
    ],
)
def test_pq_has_class(query, test_html, result):
    assert ed.pq(query).get(test_html) == result


def test_pq_strict_query_non_existent_error():
    with pytest.raises(QuerySearchResultNotFound):
        assert ed.pq_strict('[itemprop="name2"]::text').get(
            data_html.prices_and_variants,
        )


def test_pq_strict_data_empty_error():
    with pytest.raises(QuerySearchDataEmpty):
        assert ed.pq_strict('[itemprop="name"]::text').get(None)
