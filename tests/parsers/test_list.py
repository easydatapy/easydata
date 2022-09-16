import pytest

import easydata as ed
from tests.factory import data_dict, data_html, data_list

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
    "parser, test_data, result",
    [
        (
            ed.List(
                query=ed.pq("#images img::items"),
                parser=ed.Url(ed.pq("::src")),
            ),
            data_html.images,
            expected_urls,
        ),
        (
            ed.List(
                query=ed.pq("#images img::src-items"),
                parser=ed.Url(),
            ),
            data_html.images,
            expected_urls,
        ),
        (
            ed.List(
                query=ed.pq("#images img::src-items"),
                parser=None,
            ),
            data_html.images,
            expected_urls,
        ),
        (
            ed.List(
                query=None,
                parser=None,
            ),
            ["hello", "World &lt;3"],
            ["hello", "World &lt;3"],
        ),
        (
            ed.List(
                query=ed.jp("variants"),
                parser=ed.StackedParser(
                    color=ed.Text(ed.jp("color"), uppercase=True),
                    stocked=ed.Bool(ed.jp("stock")),
                ),
            ),
            data_dict.variants_data,
            [
                {"color": "BLACK", "stocked": True},
                {"color": "GRAY", "stocked": False},
            ],
        ),
        (
            ed.List(
                query=ed.jp("variants"),
                parser=ed.StackedParser(
                    color=ed.Text(ed.jp("color"), uppercase=True),
                    stocked=ed.Bool(ed.jp("stock")),
                ),
                allow_parser=ed.Has(ed.jp("color"), contains="black"),
            ),
            data_dict.variants_data,
            [
                {"color": "BLACK", "stocked": True},
            ],
        ),
        (
            ed.List(
                query=ed.jp("variants"),
                parser=ed.StackedParser(
                    color=ed.Text(ed.jp("color"), uppercase=True),
                    stocked=ed.Bool(ed.jp("stock")),
                ),
                deny_parser=ed.Has(ed.jp("color"), contains="black"),
            ),
            data_dict.variants_data,
            [
                {"color": "GRAY", "stocked": False},
            ],
        ),
        (
            ed.List(parser=ed.Url()).init_config({"ED_URL_DOMAIN": "demo.com"}),
            ["/imgs/1.jpg"],
            ["https://demo.com/imgs/1.jpg"],
        ),
        (
            ed.List(parser=ed.Url(domain="https://demo.net")).init_config(
                {"ED_URL_DOMAIN": "demo.com"}
            ),
            ["/imgs/1.jpg"],
            ["https://demo.net/imgs/1.jpg"],
        ),
        (
            ed.List(
                ed.pq("#image-container img::items"),
                parser=ed.Url(ed.pq("::src")),
                unique=True,
            ),
            data_html.images,
            expected_urls,
        ),
        (
            ed.List(
                ed.pq("#image-container img::items"),
                parser=ed.Url(ed.pq("::src")),
            ),
            data_html.images,
            expected_urls,
        ),
        (
            ed.List(
                ed.pq("#image-container img::items"),
                parser=ed.Url(ed.pq("::src")),
                unique=False,
            ),
            data_html.images,
            expected_urls_non_unique,
        ),
        (
            ed.List(
                ed.jp("options"),
                parser=ed.ItemDict(
                    name=ed.Str(ed.key("name")),
                    price=ed.Float(ed.key("price")),
                ),
            ),
            data_dict.item_with_options,
            [
                {"name": "Monitor", "price": None},
                {"name": "Mouse", "price": None},
            ],
        ),
    ],
)
def test_list(parser, test_data, result):
    assert parser.parse(test_data) == result


@pytest.mark.parametrize(
    "max_num, result",
    [
        (2, ["one", "two"]),
        (4, ["one", "two", "three", "four"]),
        (5, ["one", "two", "three", "four"]),
        (-1, ["one", "two", "three"]),
    ],
)
def test_list_max_num(max_num, result):
    list_parser = ed.List(max_num=max_num)

    assert list_parser.parse(["one", "two", "three", "four"]) == result


@pytest.mark.parametrize(
    "test_text,split_key,result",
    [
        (
            "name,surname,age,country",
            ",",
            ["name", "surname", "age", "country"],
        ),
        (
            "name,surname,age,country",
            "|",
            ["name,surname,age,country"],
        ),
        (
            "name,surname,age,country",
            ["|", ","],
            ["name", "surname", "age", "country"],
        ),
        (
            None,
            ["|", ","],
            [],
        ),
    ],
)
def test_list_split_key(test_text, split_key, result):
    list_parser = ed.List(split_key=split_key)

    assert list_parser.parse(test_text) == result


def test_list_allow_callables():
    test_text = "name,surname,age,country_code,country_group"

    list_parser = ed.List(
        parser=ed.Text(),
        split_key=",",
        preprocess_allow=lambda v, d: "country" not in v.lower(),
        process_allow=lambda v, d: "name" in v.lower(),
    )

    expected_result = ["name", "surname"]
    assert list_parser.parse(test_text) == expected_result


def test_list_allow_callables_type_error():
    test_name_list = ["name", "surname"]

    list_parser = ed.List(
        parser=ed.Text(),
        preprocess_allow=lambda v, d: None,
    )

    with pytest.raises(TypeError) as excinfo:
        list_parser.parse(test_name_list)

    assert "allow callable must return bool" in str(excinfo.value).lower()


def test_text_list():
    test_bad_char_list = ["uÌˆnicode", "Pro 13 &lt;3"]

    list_parser = ed.TextList()
    expected_result = ["ünicode", "Pro 13 <3"]
    assert list_parser.parse(test_bad_char_list) == expected_result


def test_text_list_allow():
    list_parser = ed.TextList(parser=ed.Url(), allow=["1.jp", "3.jp"])

    expected_allowed_url_list = [
        "https://demo.com/imgs/1.jpg",
        "https://demo.com/imgs/3.jpg",
    ]

    assert list_parser.parse(data_list.images) == expected_allowed_url_list


def test_text_list_callow():
    list_parser = ed.TextList(parser=ed.Url(), callow=["1.JP", "3.jp"])

    assert list_parser.parse(data_list.images) == [expected_urls[2]]


@pytest.mark.parametrize(
    "from_allow, result",
    [
        (["2.jp"], expected_urls[1:]),
        (["0.jp", "2.JP"], expected_allowed_urls),
        (["0.jp"], []),
    ],
)
def test_text_list_from_allow(from_allow, result):
    list_parser = ed.TextList(parser=ed.Url(), from_allow=from_allow)

    assert list_parser.parse(data_list.images) == result


@pytest.mark.parametrize(
    "from_callow, result",
    [
        (["1.JP", "2.jp"], expected_urls[1:]),
        (["1.JP"], []),
    ],
)
def test_text_list_from_callow(from_callow, result):
    list_parser = ed.TextList(parser=ed.Url(), from_callow=from_callow)

    assert list_parser.parse(data_list.images) == result


@pytest.mark.parametrize(
    "to_allow, result",
    [
        (["3.jp"], expected_urls[:2]),
        (["0.jp", "3.JP"], expected_urls[:2]),
        (["0.jp"], expected_urls),
    ],
)
def test_text_list_to_allow(to_allow, result):
    list_parser = ed.TextList(parser=ed.Url(), to_allow=to_allow)

    assert list_parser.parse(data_list.images) == result


@pytest.mark.parametrize(
    "to_callow, result",
    [
        (["3.jp"], expected_urls[:2]),
        (["3.JP"], expected_urls),
    ],
)
def test_text_list_to_callow(to_callow, result):
    list_parser = ed.TextList(parser=ed.Url(), to_callow=to_callow)

    assert list_parser.parse(data_list.images) == result


@pytest.mark.parametrize(
    "deny, result",
    [
        (["1.jp", "3.JP"], [expected_urls[1]]),
        (["0.jp"], expected_urls),
    ],
)
def test_text_list_deny(deny, result):
    list_parser = ed.TextList(parser=ed.Url(), deny=deny)

    assert list_parser.parse(data_list.images) == result


def test_text_list_cdeny():
    list_parser = ed.TextList(parser=ed.Url(), cdeny=["1.JP", "3.jp"])

    assert list_parser.parse(data_list.images) == expected_urls[:2]


@pytest.mark.parametrize(
    "test_text,split_key,result",
    [
        (
            "name,surname,age,country",
            ",",
            ["name", "surname", "age", "country"],
        ),
        (
            None,
            ["|", ","],
            [],
        ),
    ],
)
def test_text_list_split_key(test_text, split_key, result):
    text_list_parser = ed.TextList(split_key=split_key)

    assert text_list_parser.parse(test_text) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (["https://demo.com/imgs/1.jpg"], expected_multiplied_urls),
        (data_list.images, expected_multiplied_urls),
        ("https://demo.com/imgs/1.jpg", expected_multiplied_urls),
    ],
)
def test_text_list_multiply_keys(test_data, result):
    list_parser = ed.TextList(
        parser=ed.Text(),
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

    assert ed.UrlList().parse(bad_img_urls) == expected_fixed_img_urls


def test_url_list_config():
    # Lets test if config settings are correctly passed to a child Url parser!
    url_list_parser = ed.UrlList()
    url_list_parser.init_config({"ED_URL_DOMAIN": "demo.com"})

    assert url_list_parser.parse(["/imgs/1.jpg"]) == ["https://demo.com/imgs/1.jpg"]


def test_url_list_config_override():
    # Lets test if config settings can get overriden
    url_list_parser = ed.UrlList(domain="https://demo.net")
    url_list_parser.init_config({"ED_URL_DOMAIN": "demo.com"})

    assert url_list_parser.parse(["/imgs/1.jpg"]) == ["https://demo.net/imgs/1.jpg"]


@pytest.mark.parametrize(
    "query, result",
    [
        (
            "::html",
            [
                "info@easydatapy.com",
                "rg@easydatapy.com",
                "admin@easydatapy.com",
                "groove@easydatapy.com",
            ],
        ),
        ("p::text", ["info@easydatapy.com"]),
        ("body::text", ["info@easydatapy.com", "groove@easydatapy.com"]),
        ("div::html-items", ["rg@easydatapy.com", "admin@easydatapy.com"]),
        (
            ".first a,.second a::href-items",
            ["rg@easydatapy.com", "admin@easydatapy.com"],
        ),
        ("div a::href-items", ["rg@easydatapy.com", "admin@easydatapy.com"]),
        (".website::text", []),
    ],
)
def test_email_search_list_html(query, result):
    test_email_html = """
        <body>
            <p>Email us at: info@easydatapy.com and receive great info!</p>
            <div class="first"><a href="mailto:rg@easydatapy.com">RG</a></div>
            <div class="second"><a href="mailto:admin@easydatapy.com">admin</a></div>
            groove@easydatapy.com
            <span class="website">easydatapy.com</span>
        </body>
    """

    email_search_list_parser = ed.EmailSearchList(
        query=ed.pq(query),
    )

    assert email_search_list_parser.parse(test_email_html) == result


@pytest.mark.parametrize(
    "query, result",
    [
        (
            "::json",
            [
                "info@easydatapy.com",
                "admin@easydatapy.com",
                "rg@easydatapy.com",
                "support@easydatapy.com",
                "support2@easydatapy.com",
            ],
        ),
        (
            "::yaml",
            [
                "support@easydatapy.com",
                "support2@easydatapy.com",
                "admin@easydatapy.com",
                "rg@easydatapy.com",
                "info@easydatapy.com",
            ],
        ),
        (
            "::str",
            [
                "info@easydatapy.com",
                "admin@easydatapy.com",
                "rg@easydatapy.com",
                "support@easydatapy.com",
                "support2@easydatapy.com",
            ],
        ),
        (
            "additional_contacts",
            ["support@easydatapy.com", "support2@easydatapy.com"],
        ),
    ],
)
def test_email_search_list_dict(query, result):
    test_email_dict = {
        "main_contact": "info@easydatapy.com",
        "contacts": [
            {"email": "admin@easydatapy.com", "name": "admin"},
            {"email": "rg@easydatapy.com", "name": "RG"},
        ],
        "additional_contacts": ["support@easydatapy.com", "support2@easydatapy.com"],
    }

    email_search_list_parser = ed.EmailSearchList(query=ed.jp(query))

    assert email_search_list_parser.parse(test_email_dict) == result
