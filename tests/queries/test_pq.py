import pytest

from easydata.queries import pq

test_html = """
    <html>
        <body>
            <div class="breadcrumbs">
                <div class="breadcrumb">Home</div>
                <div class="breadcrumb">Phone</div>
                <div class="breadcrumb">Smartphone</div>
            </div>
            <h2 class="name">
                <div class="brand">EasyData</div>
                Test Product Item
            </h2>
            <input value="smartphone" content="phone" name="category" />
            <a id="url" href="http://demo.com/product/123">Item Link</a>
            <div class="images">
                <img src="http://demo.com/img1.jpg" />
                <img src="http://demo.com/img2.jpg" />
                <img src="http://demo.com/img3.jpg" />
            </div>
        </body>
    </html>
"""

exp_result_images = [
    "http://demo.com/img1.jpg",
    "http://demo.com/img2.jpg",
    "http://demo.com/img3.jpg",
]


def test_pq_query_text():
    assert pq(".brand::text").get(test_html) == "EasyData"


@pytest.mark.parametrize(
    "query, result",
    [
        (".breadcrumbs .breadcrumb::text", "Home"),
        (".breadcrumbs .breadcrumb::text-all", "Home Phone Smartphone"),
    ],
)
def test_pq_query_all(query, result):
    assert pq(query).get(test_html) == result

    assert pq(query=query).get(test_html) == result


@pytest.mark.parametrize(
    "query",
    [".images img::attr(src)-items", ".images img::src-items"],
)
def test_pq_query_items(query):
    assert pq(query).get(test_html) == exp_result_images


def test_pq_query_attr():
    exp_result = "smartphone"
    assert pq('[name="category"]::attr(value)').get(test_html) == exp_result


def test_pq_query_attr_all():
    test_all_html = '<input some-strange-value="EasyData">'
    assert pq("input::attr(some-strange-value)-all").get(test_all_html) == "EasyData"


def test_pq_query_attr_val():
    result = pq('[name="category"]::val').get(test_html)
    assert result == "smartphone"


def test_pq_query_attr_name():
    result = pq('[name="category"]::name').get(test_html)
    assert result == "category"


def test_pq_query_attr_content():
    result = pq('[name="category"]::content').get(test_html)
    assert result == "phone"


def test_pq_query_attr_src():
    result = pq(".images img::src").get(test_html)
    assert result == "http://demo.com/img1.jpg"


def test_pq_query_attr_href():
    result = pq("#url::href").get(test_html)
    assert result == "http://demo.com/product/123"


def test_pq_query_remove_query():
    exp_result = "Test Product Item"
    assert pq(".name::text", remove_query=".brand").get(test_html) == exp_result


def test_pq_query_html():
    exp_result = '<div class="brand">EasyData</div>\nTest Product Item'
    assert pq(".name::html").get(test_html).strip().replace("  ", "") == exp_result
