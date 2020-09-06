from easydata.utils import url


def test_remove_qs() -> None:
    test_url = "http://example.com/item?a=1&b=1"

    assert url.remove_qs(test_url) == "http://example.com/item"

    assert url.remove_qs(test_url, "b") == "http://example.com/item?a=1"

    assert url.remove_qs(test_url, ["a", "b"]) == "http://example.com/item"


def test_set_qs_value() -> None:
    test_url = "http://example.com/item?a=1&b=1"

    expected_url = "http://example.com/item?a=2&b=1"
    assert url.set_qs_value(test_url, "a", "2") == expected_url

    expected_url = "http://example.com/item?a=1&b=1&c=5"
    assert url.set_qs_value(test_url, "c", "5") == expected_url


def test_set_qs_values() -> None:
    test_url = "http://example.com/item?a=1&b=1"

    expected_url = "http://example.com/item?a=2&b=1&c=3"
    assert url.set_qs_values(test_url, {"a": 2, "c": 3}) == expected_url

    expected_url = "http://example.com/item?a=2&b=3"
    assert url.set_qs_values(test_url, {"a": 2, "b": 3}) == expected_url


def test_get_path() -> None:
    test_url = "http://example.com/products/item?a=1"

    assert url.get_path(test_url) == "/products/item"

    assert url.get_path(test_url, index=-1) == "item"


def test_normalize() -> None:
    test_url = "/products/item?a=1"

    expected_url = "https://example.com/products/item?a=1"
    assert url.normalize(test_url, "example.com") == expected_url

    test_url = "//example.com/products/item?a=1"

    expected_url = "https://example.com/products/item?a=1"
    assert url.normalize(test_url) == expected_url

    test_url = "//example.com/products/item?a=1"

    expected_url = "http://example.com/products/item?a=1"
    assert url.normalize(test_url, "http://example.com") == expected_url


def test_from_text() -> None:
    test_text = "Visit here: http://example.com/products/item?a=1"

    expected_url = "http://example.com/products/item?a=1"
    assert url.from_text(test_text) == expected_url


def test_from_text_multiple() -> None:
    test_text = (
        "Visit here: http://example.com/products/item?a=1 and"
        "https://example.com/products/item/ and no more!"
    )

    expected_urls = [
        "http://example.com/products/item?a=1",
        "https://example.com/products/item/",
    ]
    assert url.from_text_multiple(test_text) == expected_urls
