import pytest

from easydata import parsers
from easydata.queries import jp
from tests.factory import data_dict


@pytest.mark.parametrize(
    "string_format_parser, test_data, result",
    [
        (
            parsers.StringFormat(
                "https://demo.com/{item_path}.html?id={item_id}",
                item_path=parsers.Data(jp("url_path")),
                item_id=parsers.Data(jp("id")),
            ),
            data_dict.item_with_options,
            "https://demo.com/easybook-pro-15.html?id=123",
        ),
        (
            parsers.StringFormat(
                "https://demo.com/easybook-pro-15.html?id=123",
            ),
            data_dict.item_with_options,
            "https://demo.com/easybook-pro-15.html?id=123",
        ),
    ],
)
def test_string_format(string_format_parser, test_data, result):
    assert string_format_parser.parse(test_data) == result


def test_string_format_value_error():
    string_format_parser = parsers.StringFormat(
        "https://demo.com/{item_path}.html?id={item_id}",
        item_path=parsers.Data(jp("url_path_non_existent")),
        item_id=parsers.Data(jp("id")),
    )

    with pytest.raises(ValueError):
        string_format_parser.parse(data_dict.item_with_options)
