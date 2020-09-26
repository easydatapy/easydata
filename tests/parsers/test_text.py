import pytest

from easydata.parsers import Text


@pytest.mark.parametrize(
    "test_data, result",
    [("Easybook Pro 13", "Easybook Pro 13"), ("easybook pro 13", "easybook pro 13")],
)
def test_text_parser(test_data, result):
    assert Text().parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("Easybook Pro 13 &lt;3 uÌˆnicode", "Easybook Pro 13 <3 ünicode"),
        (" easybook pro   13", "easybook pro 13"),
        (" Easybook Pro 13    ", "Easybook Pro 13"),
        ("Easybook Pro\n13", "Easybook Pro 13"),
    ],
)
def test_text_normalize_default(test_data, result):
    assert Text().parse(test_data) == result


def test_text_normalize_false():
    text_parser = Text(normalize=False)

    expected_text = "Easybook Pro 13 &lt;3 uÌˆnicode"
    assert text_parser.parse("Easybook Pro 13 &lt;3 uÌˆnicode") == expected_text


def test_text_replace_keys():
    test_text = "Easybook Pro 15"

    item_data = Text(replace_keys=[("pro", "Air"), ("15", "13")])
    assert item_data.parse(test_text) == "Easybook Air 13"


@pytest.mark.parametrize(
    "split_key, test_data, result",
    [
        ("-", "easybook-pro_13", "easybook"),
        (("-", -1), "easybook-pro_13", "pro_13"),
    ],
)
def test_text_split_key(split_key, test_data, result):
    item_data = Text(split_key=split_key)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "split_keys, test_data, result",
    [
        ([("-", -1), "_"], "easybook-pro_13", "pro"),
    ],
)
def test_text_field_split_keys(split_keys, test_data, result):
    item_data = Text(split_keys=split_keys)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (("Easybook", "pro", 13), "Easybook pro 13"),
        (["Easybook", "pro", 13], "Easybook pro 13"),
    ],
)
def test_text_field_separator_default(test_data, result):
    item_data = Text()
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "separator, test_data, result",
    [
        ("-", ["Easybook", "pro", 13], "Easybook-pro-13"),
        (" > ", ["Easybook", "pro", 13], "Easybook > pro > 13"),
    ],
)
def test_text_field_separator_custom(separator, test_data, result):
    item_data = Text(separator=separator)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "index, test_data, result",
    [
        (0, ["Easybook", "pro", 13], "Easybook"),
        (-1, ["Easybook", "pro", 13], "13"),
    ],
)
def test_text_field_index(index, test_data, result):
    item_data = Text(index=index)
    assert item_data.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (None, None),
        ("", None),
    ],
)
def test_text_parser_empty_data(test_data, result):
    text_parser = Text()
    assert text_parser.parse(test_data) is result


@pytest.mark.parametrize(
    "default, test_data, result",
    [
        ("Default Item", None, "Default Item"),
        ("", None, ""),
    ],
)
def test_text_parser_default(default, test_data, result):
    text_parser = Text(default=default)
    assert text_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "take, test_data, result",
    [
        (8, "Easybook Pro 13", "Easybook"),
        (30, "Easybook Pro 13", "Easybook Pro 13"),
    ],
)
def test_text_take(take, test_data, result):
    text_parser = Text(take=take)
    assert text_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "skip, test_data, result",
    [
        (8, "Easybook Pro 13", "Pro 13"),
        (30, "Easybook Pro 13", None),
    ],
)
def test_text_skip(skip, test_data, result):
    text_parser = Text(skip=skip)
    assert text_parser.parse(test_data) == result


def test_text_parser_uppercase():
    text_parser = Text(uppercase=True)
    assert text_parser.parse("Easybook Pro 13") == "EASYBOOK PRO 13"


def test_text_parser_lowercase():
    text_parser = Text(lowercase=True)
    assert text_parser.parse("Easybook Pro 13") == "easybook pro 13"


def test_text_parser_title():
    text_parser = Text(title=True)
    assert text_parser.parse("Easybook Pro 13") == "Easybook Pro 13"


def test_text_parser_capitalize():
    text_parser = Text(capitalize=True)
    assert text_parser.parse("Easybook pro 13") == "Easybook pro 13"
