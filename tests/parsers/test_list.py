import pytest

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

expected_urls_max_2 = [
    "https://demo.com/imgs/1.jpg",
    "https://demo.com/imgs/2.jpg",
]

expected_allowed_urls = [
    "https://demo.com/imgs/2.jpg",
    "https://demo.com/imgs/3.jpg",
]

expected_multiplied_urls = [
    "https://demo.com/imgs/1.jpg",
    "https://demo.com/imgs/2.jpg",
    "https://demo.com/imgs/3.jpg",
    "https://demo.com/imgs/4.jpg",
]


@pytest.mark.parametrize(
    "query, parser, test_data, result",
    [
        (pq("#images img::items"), parsers.Url(pq("::src")), db, expected_urls),
        (pq("#images img::src-items"), parsers.Url(), db, expected_urls),
        (pq("#images img::src-items"), None, db, expected_urls),
        (None, None, ["hello", "World &lt;3"], ["hello", "World &lt;3"]),
    ],
)
def test_list(query, parser, test_data, result):
    list_parser = parsers.List(query=query, parser=parser)

    assert list_parser.parse(test_data) == result


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


def test_list_allow_callables():
    test_text = "name,surname,age,country_code,country_group"

    list_parser = parsers.List(
        parser=parsers.Text(),
        split_key=",",
        preprocess_allow=lambda v, d: "country" not in v.lower(),
        process_allow=lambda v, d: "name" in v.lower(),
    )

    expected_result = ["name", "surname"]
    assert list_parser.parse(test_text) == expected_result


def test_list_allow_callables_type_error():
    test_name_list = ["name", "surname"]

    list_parser = parsers.List(
        parser=parsers.Text(),
        preprocess_allow=lambda v, d: None,
    )

    with pytest.raises(TypeError) as excinfo:
        list_parser.parse(test_name_list)

    assert "allow callable must return bool" in str(excinfo.value).lower()


def test_text_list():
    test_bad_char_list = ["uÌˆnicode", "Pro 13 &lt;3"]

    list_parser = parsers.TextList()
    expected_result = ["ünicode", "Pro 13 <3"]
    assert list_parser.parse(test_bad_char_list) == expected_result


def test_text_list_allow():
    list_parser = parsers.TextList(parser=parsers.Url(), allow=["1.jp", "3.jp"])

    expected_allowed_url_list = [
        "https://demo.com/imgs/1.jpg",
        "https://demo.com/imgs/3.jpg",
    ]

    assert list_parser.parse(test_img_url_list) == expected_allowed_url_list


def test_text_list_callow():
    list_parser = parsers.TextList(parser=parsers.Url(), callow=["1.JP", "3.jp"])

    assert list_parser.parse(test_img_url_list) == [expected_urls[2]]


@pytest.mark.parametrize(
    "from_allow, result",
    [
        (["2.jp"], expected_urls[1:]),
        (["0.jp", "2.JP"], expected_allowed_urls),
        (["0.jp"], []),
    ],
)
def test_text_list_from_allow(from_allow, result):
    list_parser = parsers.TextList(parser=parsers.Url(), from_allow=from_allow)

    assert list_parser.parse(test_img_url_list) == result


@pytest.mark.parametrize(
    "from_callow, result",
    [
        (["1.JP", "2.jp"], expected_urls[1:]),
        (["1.JP"], []),
    ],
)
def test_text_list_from_callow(from_callow, result):
    list_parser = parsers.TextList(parser=parsers.Url(), from_callow=from_callow)

    assert list_parser.parse(test_img_url_list) == result


@pytest.mark.parametrize(
    "to_allow, result",
    [
        (["3.jp"], expected_urls[:2]),
        (["0.jp", "3.JP"], expected_urls[:2]),
        (["0.jp"], expected_urls),
    ],
)
def test_text_list_to_allow(to_allow, result):
    list_parser = parsers.TextList(parser=parsers.Url(), to_allow=to_allow)

    assert list_parser.parse(test_img_url_list) == result


@pytest.mark.parametrize(
    "to_callow, result",
    [
        (["3.jp"], expected_urls[:2]),
        (["3.JP"], expected_urls),
    ],
)
def test_text_list_to_callow(to_callow, result):
    list_parser = parsers.TextList(parser=parsers.Url(), to_callow=to_callow)

    assert list_parser.parse(test_img_url_list) == result


@pytest.mark.parametrize(
    "deny, result",
    [
        (["1.jp", "3.JP"], [expected_urls[1]]),
        (["0.jp"], expected_urls),
    ],
)
def test_text_list_deny(deny, result):
    list_parser = parsers.TextList(parser=parsers.Url(), deny=deny)

    assert list_parser.parse(test_img_url_list) == result


def test_text_list_cdeny():
    list_parser = parsers.TextList(parser=parsers.Url(), cdeny=["1.JP", "3.jp"])

    assert list_parser.parse(test_img_url_list) == expected_urls[:2]


@pytest.mark.parametrize(
    "test_data, result",
    [
        (["https://demo.com/imgs/1.jpg"], expected_multiplied_urls),
        (test_img_url_list, expected_multiplied_urls),
        ("https://demo.com/imgs/1.jpg", expected_multiplied_urls),
    ],
)
def test_text_list_multiply_keys(test_data, result):
    list_parser = parsers.TextList(
        parser=parsers.Text(),
        multiply_keys=[("1.jpg", ["1.jpg", "2.jpg", "3.jpg", "4.jpg"])],
    )

    assert list_parser.parse(test_data) == result


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
