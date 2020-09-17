import json

import pytest
from pyquery import PyQuery

from easydata import parsers, processors
from easydata.data import VariantsData
from easydata.queries import jp, key, pq
from tests.factory import dict_data, html_data


@pytest.mark.parametrize(
    "source, data_type",
    [
        ("data", PyQuery),
        ("data_raw", str),
    ],
)
def test_data_processor(source, data_type):
    db = processors.DataProcessor(
        process_source_data=lambda source_data: PyQuery(source_data)
    ).parse_data(html_data.with_paragraph_text)

    assert isinstance(db[source], data_type)


@pytest.mark.parametrize(
    "source, data_type",
    [
        ("data", PyQuery),
        ("data_raw", str),
    ],
)
def test_data_to_pq_processor(source, data_type):
    db = processors.DataToPqProcessor().parse_data(html_data.with_paragraph_text)

    assert isinstance(db[source], data_type)


@pytest.mark.parametrize(
    "new_source, source, data_type",
    [
        ("data_pq", "data_pq", PyQuery),
        ("data_pq", "data", str),
    ],
)
def test_data_to_pq_processor_new_source(new_source, source, data_type):
    db = processors.DataToPqProcessor(
        new_source=new_source,
    ).parse_data(html_data.with_paragraph_text)

    assert isinstance(db[source], data_type)


def test_data_from_query_processor():
    test_dict = {"info": {"title": "EasyBook"}}

    db = processors.DataFromQueryProcessor(jp("info")).parse_data(test_dict)

    assert db["data"]["title"] == "EasyBook"


def test_data_from_re_processor():
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataTextFromReProcessor(
        query=r"var config = (.*?);",
        new_source="config_json",
    )

    db = data_processor.parse_data(test_text)

    assert json.loads(db["config_json"])["title"] == "EasyBook"


@pytest.mark.parametrize(
    "query, dotall, ignore_case, result",
    [
        ("spConfig = (.*?);", True, False, "149.95"),
        ("spConfig = (.*?);", False, False, None),
        ("spconfig = (.*?);", True, True, "149.95"),
    ],
)
def test_data_from_re_processor_dotall_ignore_case(
    query,
    dotall,
    ignore_case,
    result,
):

    json_text = """
    let spConfig = {
        "basePrice": "149.95"
    };
    """

    data_processor = processors.DataTextFromReProcessor(
        query=query,
        dotall=dotall,
        ignore_case=ignore_case,
        none_if_empty=True,
    )

    db = data_processor.parse_data(json_text)

    if db["data"]:
        json_data = json.loads(db["data"])

        assert json_data["basePrice"] == result
    else:
        assert db["data"] == result


def test_data_from_re_processor_none():
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataTextFromReProcessor(
        query=r"var config_wrong = (.*?);",
        new_source="config_json",
        none_if_empty=True,
    )

    json_dict = data_processor.parse_data(test_text)

    assert json_dict["config_json"] is None


def test_data_json_from_re_to_dict_processor():
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataJsonFromReToDictProcessor(
        query=r"var config = (.*?);",
        new_source="config_json",
    )

    json_dict = data_processor.parse_data(test_text)

    assert json_dict["config_json"]["title"] == "EasyBook"


def test_data_variants_processor():
    db = processors.DataVariantsProcessor(
        query=jp("variants"), key_query=key("color")
    ).parse_data(dict_data.with_variants_data)

    assert isinstance(db["variant_data"], VariantsData)

    assert len(db["variant_data"]) == 2

    assert list(db["variant_data"].keys())[0] == "Black"

    assert list(db["variant_data"].variants())[0] == {"color": "Black", "stock": True}


def test_data_variants_processor_html():
    # Lets test with HTML data and pq selector
    db = processors.DataVariantsProcessor(
        query=pq("#color-variants .color::items"),
        key_parser=parsers.Text(pq("::text"), uppercase=True),
    ).parse_data(html_data.with_prices_and_variants)

    assert isinstance(db["variant_data"], VariantsData)

    assert len(db["variant_data"]) == 2

    assert list(db["variant_data"].keys())[0] == "BLACK"


def test_data_variants_processor_multi_values():
    # Lets test with multi_values set to True
    db = processors.DataVariantsProcessor(
        query=jp("variants"), key_query=key("color")
    ).parse_data(dict_data.with_variants_data_multi)

    assert isinstance(db["variant_data"], VariantsData)

    assert len(db["variant_data"]) == 2

    assert list(db["variant_data"].keys())[0] == "Black"

    expected_values_result = [
        {"color": "Black", "size": "13", "stock": True},
        {"color": "Black", "size": "15", "stock": True},
    ]
    assert db["variant_data"]["Black"] == expected_values_result

    assert list(db["variant_data"].values())[0] == expected_values_result

    assert db["variant_data"].variants()[0] == expected_values_result[0]
