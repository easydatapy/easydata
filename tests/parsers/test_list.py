from easydata import parsers
from easydata.queries import pq
from tests.factory import load_data_bag_with_pq

db = load_data_bag_with_pq("product")

test_dict_text = {
    "images": [
        {"src": "https://demo.com/imgs/1.jpg"},
        {"src": "https://demo.com/imgs/2.jpg"},
        {"src": "https://demo.com/imgs/3.jpg"},
    ]
}

test_img_url_list = [
    "https://demo.com/imgs/1.jpg",
    "https://demo.com/imgs/2.jpg",
    "https://demo.com/imgs/3.jpg",
]

expected_urls = [
    "https://demo.com/imgs/1.jpg",
    "https://demo.com/imgs/2.jpg",
    "https://demo.com/imgs/3.jpg",
]

expected_urls_non_unique = [
    "https://demo.com/imgs/1.jpg",
    "https://demo.com/imgs/1.jpg",
    "https://demo.com/imgs/2.jpg",
    "https://demo.com/imgs/3.jpg",
]

expected_urls_max_2 = ["https://demo.com/imgs/1.jpg", "https://demo.com/imgs/2.jpg"]


def test_list():
    list_parser = parsers.List(pq("#images img::items"), parsers.Url(pq("::src")))

    assert list_parser.parse(db) == expected_urls

    list_parser = parsers.List(pq("#images img::src-items"), parsers.Url())

    assert list_parser.parse(db) == expected_urls

    list_parser = parsers.List(pq("#images img::src-items"))

    assert list_parser.parse(db) == expected_urls

    test_list_values = ["hello", "World &lt;3"]
    assert parsers.List().parse(test_list_values) == ["hello", "World &lt;3"]


def test_list_unique_true():
    list_parser = parsers.List(
        pq("#image-container img::items"), parsers.Url(pq("::src")), unique=True
    )

    assert list_parser.parse(db) == expected_urls


def test_list_unique_default():
    list_parser = parsers.List(
        pq("#image-container img::items"),
        parsers.Url(pq("::src")),
    )

    assert list_parser.parse(db) == expected_urls


def test_list_unique_false():
    list_parser = parsers.List(
        pq("#image-container img::items"), parsers.Url(pq("::src")), unique=False
    )

    assert list_parser.parse(db) == expected_urls_non_unique


def test_list_max_num():
    list_parser = parsers.List(
        pq("#image-container img::items"), parsers.Url(pq("::src")), max_num=2
    )

    assert list_parser.parse(db) == expected_urls_max_2


def test_list_split_key():
    test_text = "name,surname,age,country"

    list_parser = parsers.List(parser=parsers.Text(), split_key=",")

    expected_result = ["name", "surname", "age", "country"]
    assert list_parser.parse(test_text) == expected_result


def test_text_list():
    test_bad_char_list = ["uÌˆnicode", "Pro 13 &lt;3"]

    list_parser = parsers.TextList()
    expected_result = ["ünicode", "Pro 13 <3"]
    assert list_parser.parse(test_bad_char_list) == expected_result


def test_text_list_allow():
    list_parser = parsers.TextList(parser=parsers.Url(), allow=["1.jp", "3.jp"])

    expected_allowed_urls = [
        "https://demo.com/imgs/1.jpg",
        "https://demo.com/imgs/3.jpg",
    ]

    assert list_parser.parse(test_img_url_list) == expected_allowed_urls


def test_text_list_callow():
    list_parser = parsers.TextList(parser=parsers.Url(), callow=["1.JP", "3.jp"])

    assert list_parser.parse(test_img_url_list) == [expected_urls[2]]


def test_text_list_from_allow():
    list_parser = parsers.TextList(parser=parsers.Url(), from_allow=["2.jp"])

    expected_allowed_urls = [
        "https://demo.com/imgs/2.jpg",
        "https://demo.com/imgs/3.jpg",
    ]

    assert list_parser.parse(test_img_url_list) == expected_urls[1:]

    list_parser = parsers.TextList(parser=parsers.Url(), from_allow=["0.jp", "2.JP"])

    assert list_parser.parse(test_img_url_list) == expected_allowed_urls

    list_parser = parsers.TextList(parser=parsers.Url(), from_allow=["0.jp"])

    assert list_parser.parse(test_img_url_list) == []


def test_text_list_from_callow():
    list_parser = parsers.TextList(parser=parsers.Url(), from_callow=["1.JP", "2.jp"])

    assert list_parser.parse(test_img_url_list) == expected_urls[1:]

    list_parser = parsers.TextList(parser=parsers.Url(), from_callow=["1.JP"])

    assert list_parser.parse(test_img_url_list) == []


def test_text_list_to_allow():
    list_parser = parsers.TextList(parser=parsers.Url(), to_allow=["3.jp"])

    assert list_parser.parse(test_img_url_list) == expected_urls[:2]

    list_parser = parsers.TextList(parser=parsers.Url(), to_allow=["0.jp", "3.JP"])

    assert list_parser.parse(test_img_url_list) == expected_urls[:2]

    list_parser = parsers.TextList(parser=parsers.Url(), to_allow=["0.jp"])

    assert list_parser.parse(test_img_url_list) == expected_urls


def test_text_list_to_callow():
    list_parser = parsers.TextList(parser=parsers.Url(), to_callow=["3.jp"])

    assert list_parser.parse(test_img_url_list) == expected_urls[:2]

    list_parser = parsers.TextList(parser=parsers.Url(), to_callow=["3.JP"])

    assert list_parser.parse(test_img_url_list) == expected_urls


def test_text_list_deny():
    list_parser = parsers.TextList(parser=parsers.Url(), deny=["1.jp", "3.JP"])

    assert list_parser.parse(test_img_url_list) == [expected_urls[1]]

    list_parser = parsers.TextList(parser=parsers.Url(), deny=["0.jp"])

    assert list_parser.parse(test_img_url_list) == expected_urls


def test_text_list_cdeny():
    list_parser = parsers.TextList(parser=parsers.Url(), cdeny=["1.JP", "3.jp"])

    assert list_parser.parse(test_img_url_list) == expected_urls[:2]


def test_text_list_multiply_keys():
    test_image_urls = ["https://demo.com/imgs/1.jpg"]

    list_parser = parsers.TextList(
        parser=parsers.Text(),
        multiply_keys=[("1.jpg", ["1.jpg", "2.jpg", "3.jpg", "4.jpg"])],
    )

    expected_multiplied_urls = [
        "https://demo.com/imgs/1.jpg",
        "https://demo.com/imgs/2.jpg",
        "https://demo.com/imgs/3.jpg",
        "https://demo.com/imgs/4.jpg",
    ]

    assert list_parser.parse(test_image_urls) == expected_multiplied_urls

    assert list_parser.parse(test_img_url_list) == expected_multiplied_urls

    test_text = "https://demo.com/imgs/1.jpg"

    assert list_parser.parse(test_text) == expected_multiplied_urls


def test_url_list():
    bad_img_urls = [
        "https://demo.com/imgs/1.jpg",
        "://demo.com/imgs/2.jpg",
        "demo.com/imgs/3.jpg",
        "//demo.com/imgs/4.jpg",
    ]

    expected_fixed_img_urls = [
        "https://demo.com/imgs/1.jpg",
        "https://demo.com/imgs/2.jpg",
        "https://demo.com/imgs/3.jpg",
        "https://demo.com/imgs/4.jpg",
    ]

    assert parsers.UrlList().parse(bad_img_urls) == expected_fixed_img_urls
