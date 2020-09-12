import json

import pytest
from pyquery import PyQuery

from easydata import processors
from easydata.queries import jp, key, pq

test_html_text = "<p>Sample text</p>"

test_variants_data = {
    "title": "EasyData Pro 13",
    "variants": [
        {"color": "Black", "stock": True},
        {"color": "Gray", "stock": False},
    ],
}

test_variants_data_multi = {
    "title": "EasyData Pro",
    "variants": [
        {"color": "Black", "size": "13", "stock": True},
        {"color": "Black", "size": "15", "stock": True},
        {"color": "Gray", "size": "13", "stock": False},
        {"color": "Gray", "size": "15", "stock": True},
    ],
}

test_variants_html_data = """
    <p>EasyBook Pro 15</p>
    <div id="color-variants">
        Colors:
        <div class="color" stock="true">
            <span class="color-name">Black</span>
            <img src="https://demo.com/imgs/black-1.jpg">
        </div>
        <div class="color" stock="false">
            <span>Gray</span>
            <img src="https://demo.com/imgs/black-1.jpg">
        </div>
    </div>
"""


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
    ).parse_data(test_html_text)

    assert isinstance(db[source], data_type)


@pytest.mark.parametrize(
    "source, data_type",
    [
        ("data", PyQuery),
        ("data_raw", str),
    ],
)
def test_data_to_pq_processor(source, data_type):
    db = processors.DataToPqProcessor().parse_data(test_html_text)

    assert isinstance(db[source], data_type)


@pytest.mark.parametrize(
    "new_source, source, data_type",
    [
        ("data_pq", "data_pq", PyQuery),
        ("data_pq", "data", str),
    ],
)
def test_data_to_pq_processor_new_source(new_source, source, data_type):
    db = processors.DataToPqProcessor(new_source=new_source).parse_data(test_html_text)

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


def test_data_variant_processor():
    db = processors.DataVariantProcessor(
        query=jp("variants"), variant_query=key("color")
    ).parse_data(test_variants_data)

    assert isinstance(db["data_variants"], dict)

    assert len(db["data_variants"]) == 2

    assert list(db["data_variants"].keys())[0] == "black"

    expected_values_result = {"color": "Black", "stock": True}

    assert list(db["data_variants"].values())[0] == expected_values_result


def test_data_variant_processor_multi_values():
    # Lets test with multi_values set to True
    db = processors.DataVariantProcessor(
        query=jp("variants"), variant_query=key("color"), multi_values=True
    ).parse_data(test_variants_data_multi)

    assert isinstance(db["data_variants"], dict)

    assert len(db["data_variants"]) == 2

    assert list(db["data_variants"].keys())[0] == "black"

    expected_values_result = [
        {"color": "Black", "size": "13", "stock": True},
        {"color": "Black", "size": "15", "stock": True},
    ]
    assert list(db["data_variants"].values())[0] == expected_values_result

    # Lets test with HTML data and pq selector
    db = processors.DataVariantProcessor(
        query=pq("#color-variants .color::items"), variant_query=pq("::text")
    ).parse_data(test_variants_html_data)

    assert isinstance(db["data_variants"], dict)

    assert len(db["data_variants"]) == 2

    assert list(db["data_variants"].keys())[0] == "black"


def test_data_variant_processor_lower_false():
    db = processors.DataVariantProcessor(
        query=key("variants"),
        variant_query=jp("color"),
        variant_values_lower=False,
        multi_values=True,
    ).parse_data(test_variants_data_multi)

    assert list(db["data_variants"].keys())[0] == "Black"


def test_data_variant_processor_with_variant_values_false():
    db = processors.DataVariantProcessor(
        query=key("variants"),
        variant_query=jp("color"),
        with_variant_values=False,
        multi_values=True,
    ).parse_data(test_variants_data_multi)

    assert isinstance(db["data_variants"], list)

    assert len(db["data_variants"]) == 2

    assert db["data_variants"][0][0]["color"] == "Black"
