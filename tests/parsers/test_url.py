import pytest

from easydata.parsers import Url

test_url_with_qs = "https://demo.com/?home=true"
test_url_partial = "/product/1122"
test_url_missing_protocol = "//demo.com/product/1122"


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Home url is:  https://demo.com/home  !!!", "https://demo.com/home"),
    ],
)
def test_url_from_text(test_data, result):
    url_parser = Url(from_text=True)
    assert url_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "qs, test_data, result",
    [
        ({"home": "false"}, test_url_with_qs, "https://demo.com/?home=false"),
        ({"country": "SI"}, test_url_with_qs, "https://demo.com/?home=true&country=SI"),
    ],
)
def test_url_qs(qs, test_data, result):
    url_parser = Url(qs=qs)
    assert url_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "remove_qs, test_data, result",
    [
        (True, test_url_with_qs, "https://demo.com/"),
        ("home", test_url_with_qs, "https://demo.com/"),
        (["home"], test_url_with_qs, "https://demo.com/"),
        (True, None, None),
        (True, "", None),
    ],
)
def test_url_remove_qs(remove_qs, test_data, result):
    url_parser = Url(remove_qs=remove_qs)
    assert url_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "default, test_data, result",
    [
        ("http://demo.com", None, "http://demo.com"),
        ("http://demo.com", "", "http://demo.com"),
    ],
)
def test_url_default_value(default, test_data, result):
    url_parser = Url(default=default)
    assert url_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "domain, test_data, result",
    [
        ("demo.com", test_url_partial, "https://demo.com/product/1122"),
        ("http://demo.com", test_url_partial, "http://demo.com/product/1122"),
    ],
)
def test_url_domain(domain, test_data, result):
    url_parser = Url(domain=domain)
    assert url_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_url_missing_protocol, "https://demo.com/product/1122"),
    ],
)
def test_url_normalize(test_data, result):
    url_parser = Url(normalize=True)
    assert url_parser.parse(test_data) == result


def test_url_config():
    url_parser = Url()

    url_parser.init_config({"ED_URL_DOMAIN": "demo.com"})
    expected_url = "https://demo.com/product/1122"
    assert url_parser.parse(test_url_partial) == expected_url

    url_parser.init_config({"ED_URL_DOMAIN": "demo.com", "ED_URL_PROTOCOL": "ftp"})
    expected_url = "ftp://demo.com/product/1122"
    assert url_parser.parse(test_url_partial) == expected_url
