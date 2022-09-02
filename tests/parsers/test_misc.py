import pytest

import easydata as ed
from tests.factory import data_dict


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (
            ed.StringFormat(
                "https://demo.com/{item_path}.html?id={item_id}",
                item_path=ed.Data(ed.jp("url_path")),
                item_id=ed.Data(ed.jp("id")),
            ),
            data_dict.item_with_options,
            "https://demo.com/easybook-pro-15.html?id=123",
        ),
        (
            ed.StringFormat("https://demo.com/easybook-pro-15.html?id=123"),
            data_dict.item_with_options,
            "https://demo.com/easybook-pro-15.html?id=123",
        ),
    ],
)
def test_string_format(parser, test_data, result):
    assert parser.parse(test_data) == result


def test_string_format_value_error():
    string_format_parser = ed.StringFormat(
        "https://demo.com/{item_path}.html?id={item_id}",
        item_path=ed.Data(ed.jp("url_path_non_existent")),
        item_id=ed.Data(ed.jp("id")),
    )

    with pytest.raises(ValueError):
        string_format_parser.parse(data_dict.item_with_options)
