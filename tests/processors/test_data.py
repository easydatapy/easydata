import json

import pytest
from pyquery import PyQuery

from easydata import parsers, processors
from easydata.queries import jp, key, pq
from tests.factory import data_dict, data_html

html_paragraph_text = "<p>Sample text</p>"


@pytest.mark.parametrize(
    "source, data_type",
    [
        ("main", PyQuery),
        ("main_raw", str),
    ],
)
def test_data_processor(source, data_type):
    db = next(
        processors.DataProcessor(
            process_source_data=lambda source_data: PyQuery(source_data)
        ).parse_data(html_paragraph_text)
    )

    assert isinstance(db[source], data_type)


@pytest.mark.parametrize(
    "source, data_type",
    [
        ("main", PyQuery),
        ("main_raw", str),
    ],
)
def test_data_to_pq_processor(source, data_type):
    db = next(processors.DataToPqProcessor().parse_data(html_paragraph_text))

    assert isinstance(db[source], data_type)


@pytest.mark.parametrize(
    "new_source, source, data_type",
    [
        ("main_pq", "main_pq", PyQuery),
        ("main_pq", "main", str),
    ],
)
def test_data_to_pq_processor_new_source(new_source, source, data_type):
    db = next(
        processors.DataToPqProcessor(
            new_source=new_source,
        ).parse_data(html_paragraph_text)
    )

    assert isinstance(db[source], data_type)


def test_data_from_query_processor():
    test_dict = {"info": {"title": "EasyBook"}}

    db = next(processors.DataFromQueryProcessor(jp("info")).parse_data(test_dict))

    assert db["main"]["title"] == "EasyBook"


def test_data_from_re_processor():
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataTextFromReProcessor(
        query=r"var config = (.*?);",
        new_source="config_json",
    )

    db = next(data_processor.parse_data(test_text))

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

    db = next(data_processor.parse_data(json_text))

    if db["main"]:
        json_data = json.loads(db["main"])

        assert json_data["basePrice"] == result
    else:
        assert db["main"] == result


def test_data_from_re_processor_none():
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataTextFromReProcessor(
        query=r"var config_wrong = (.*?);",
        new_source="config_json",
        none_if_empty=True,
    )

    json_dict = next(data_processor.parse_data(test_text))

    assert json_dict["config_json"] is None


def test_data_json_to_dict_processors():
    data_processor = processors.DataJsonToDictProcessor()

    json_dict = next(data_processor.parse_data('{"title": "EasyBook"}'))

    assert json_dict["main"]["title"] == "EasyBook"


def test_data_yaml_to_dict_processors():
    test_text = """
    name: 'Item data'
    info:
      title: 'Macbook Pro 13'
      price: 999.8989
    """

    data_processor = processors.DataYamlToDictProcessor()

    json_dict = next(data_processor.parse_data(test_text))

    assert json_dict["main"]["info"]["title"] == "Macbook Pro 13"


def test_data_json_from_re_to_dict_processor():
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataJsonFromReToDictProcessor(
        query=r"var config = (.*?);",
        new_source="config_json",
    )

    json_dict = next(data_processor.parse_data(test_text))

    assert json_dict["config_json"]["title"] == "EasyBook"


def test_data_variants_processor():
    iter_db = processors.DataVariantsProcessor(
        query=jp("variants"),
        key_query=key("color"),
    ).parse_data(data_dict.variants_data)

    db_list = list(iter_db)

    assert len(db_list) == 2

    assert list(db_list[0]["main"].values())[0] == "Black"

    assert db_list[0]["main"] == {"color": "Black", "stock": True}


def test_data_variants_processor_html():
    # Lets test with HTML data and pq selector
    iter_db = processors.DataVariantsProcessor(
        query=pq("#color-variants .color::items"),
        key_parser=parsers.Text(pq("::text"), uppercase=True),
        new_source="color_data",
    ).parse_data(data_html.prices_and_variants)

    db_list = list(iter_db)

    assert len(db_list) == 2

    assert db_list[0]["color_data"].text() == "Black"

    assert db_list[0]["color_data_key"] == "BLACK"

    assert db_list[0]["color_data_variants_len"] == 2


def test_data_variants_processor_multi_values():
    # Lets test with multi_values set to True
    iter_db = processors.DataVariantsProcessor(
        query=jp("data.variants"),
        key_query=key("color"),
        new_source="color_data",
    ).parse_data(data_dict.variants_data_multi)

    db_list = list(iter_db)

    assert len(db_list) == 2

    assert list(db_list[0]["color_data"].values())[0] == "Black"

    expected_values_result = [
        {"color": "Black", "size": "13", "stock": True},
        {"color": "Black", "size": "15", "stock": True},
    ]
    assert db_list[0]["color_data_variants"] == expected_values_result
