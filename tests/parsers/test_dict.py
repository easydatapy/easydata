import pytest

from easydata import parsers
from easydata.queries import jp, pq

test_html = """
    <ul id="size-variants">
        <li size-stock="true" class="in-stock">
            <input class="size-variant" value="l">
            l
        </li>
        <li size-stock="false">
            <input class="size-variant" value="xl">
            xl
        </li>
        <li size-stock="true" class="in-stock">
            <input class="size-variant" value="xxl">
            xxl
        </li>
    </ul>
"""

test_dict_sizes = {"sizes": {"l": True, "xl": False, "xxl": True}}


def test_dict():
    dict_parser = parsers.Dict(
        pq("#size-variants li::items"),
        key_parser=parsers.Text(pq("::text")),
        value_parser=parsers.Bool(pq("::attr(size-stock)"), contains=["true"]),
    )

    expected_result = {"l": True, "xl": False, "xxl": True}
    assert dict_parser.parse(test_html) == expected_result

    dict_parser = parsers.Dict(
        pq("#size-variants li::items"),
        key_query=pq("::text"),
        value_parser=parsers.Bool(pq("::attr(size-stock)"), contains=["true"]),
    )

    assert dict_parser.parse(test_html) == expected_result

    dict_parser = parsers.Dict(
        pq("#size-variants li::items"),
        key_query=pq("::text"),
        value_query=pq("::attr(size-stock)"),
    )

    expected_text_result = {"l": "true", "xl": "false", "xxl": "true"}
    assert dict_parser.parse(test_html) == expected_text_result

    dict_parser = parsers.Dict(
        jp("sizes"), key_parser=parsers.Text(), value_parser=parsers.Bool()
    )

    assert dict_parser.parse(test_dict_sizes) == expected_result

    dict_parser = parsers.Dict(jp("sizes"))

    assert dict_parser.parse(test_dict_sizes) == expected_result

    dict_parser = parsers.Dict(jp("sizes"), key_parser=parsers.Text())

    assert dict_parser.parse(test_dict_sizes) == expected_result

    dict_parser = parsers.Dict(jp("sizes"), value_parser=parsers.Bool())

    assert dict_parser.parse(test_dict_sizes) == expected_result

    dict_parser = parsers.Dict(
        jp("sizes"), key_parser=parsers.Text(), value_parser=parsers.Text()
    )

    expected_result = {"l": "True", "xl": "False", "xxl": "True"}
    assert dict_parser.parse(test_dict_sizes) == expected_result


def test_bool_dict():
    bool_dict_parser = parsers.BoolDict(
        pq("#size-variants li::items"),
        key_query=pq("::text"),
        value_query=pq("::attr(size-stock)"),
    )

    expected_text_result = {"l": True, "xl": False, "xxl": True}
    assert bool_dict_parser.parse(test_html) == expected_text_result


@pytest.mark.parametrize(
    "test_data, result",
    [
        ({"l": True, "xl": False}, {"l": True, "xl": False}),
        ({"l": 12, "xl": 0}, {"l": True, "xl": False}),
        ({"l": "true", "xl": "false"}, {"l": True, "xl": False}),
        ({"l": "True", "xl": "False"}, {"l": True, "xl": False}),
        ({"l": "n/a", "xl": "12"}, {"l": False, "xl": False}),
    ],
)
def test_bool_dict_various_types(test_data, result):
    bool_dict_parser = parsers.BoolDict()
    assert bool_dict_parser.parse(test_data) == result
