from easydata.queries import pq

test_html = """
    <html>
        <body>
            <h2 class="name">
                <div class="brand">EasyData</div>
                Test Product Item
            </h2>
            <input value="smartphone" name="category" />
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


def test_pq_query_get_text():
    assert pq(".brand").text.get(test_html) == "EasyData"
    assert pq(".brand", text=True).get(test_html) == "EasyData"


def test_pq_query_get_attr():
    exp_result = "smartphone"
    assert pq('[name="category"]').attr("value").get(test_html) == exp_result
    assert pq('[name="category"]', attr="value").get(test_html) == exp_result


def test_pq_query_get_val():
    result = pq('[name="category"]').val.get(test_html)
    assert result == "smartphone"


def test_pq_query_get_src():
    result = pq(".images img").src.get(test_html)
    assert result == "http://demo.com/img1.jpg"


def test_pq_query_get_href():
    result = pq("#url").href.get(test_html)
    assert result == "http://demo.com/product/123"


def test_pq_query_get_rm():
    exp_result = "Test Product Item"
    assert pq(".name", rm=".brand").text.get(test_html) == exp_result


def test_pq_query_get_rm_method():
    exp_result = "Test Product Item"
    assert pq(".name").rm(".brand").text.get(test_html) == exp_result


def test_pq_query_get_html():
    exp_result = '<div class="brand">EasyData</div>\nTest Product Item'
    assert pq(".name").html.get(test_html).strip().replace("  ", "") == exp_result
    assert pq(".name", html=True).get(test_html).strip().replace("  ", "") == exp_result


def test_pq_query_get_all_src():
    assert pq(".images img").src.get_all(test_html) == exp_result_images


def test_pq_query_get_iter_src():
    assert list(pq(".images img").src.get_iter(test_html)) == exp_result_images
