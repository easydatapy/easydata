from easydata.queries import jp
from tests import factory

jd = factory.load_data_bag_with_json("product")


def test_jp_query_get():
    jp_query = jp("product_type")

    assert jp_query.get(jd, "data") == "smartphone"


def test_jp_query_get_iter():
    jp_query = jp("images[].zoom")

    expected_image_list = [
        "https://demo.com/imgs/1-zoom.jpg",
        "https://demo.com/imgs/2-zoom.jpg",
    ]
    image_list = [i for i in jp_query.get_iter(jd, "data")]

    assert image_list == expected_image_list
