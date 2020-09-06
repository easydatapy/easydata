import json

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


def test_data_processor() -> None:
    db = processors.DataProcessor(
        process_source_data=lambda source_data: PyQuery(source_data)
    ).parse_data(test_html_text)

    assert isinstance(db["data"], PyQuery)

    assert isinstance(db["data_raw"], str)


def test_data_to_pq_processor() -> None:
    db = processors.DataToPqProcessor().parse_data(test_html_text)

    assert isinstance(db["data"], PyQuery)

    assert isinstance(db["data_raw"], str)


def test_data_to_pq_processor_new_source() -> None:
    db = processors.DataToPqProcessor(new_source="data_pq").parse_data(test_html_text)

    assert isinstance(db["data_pq"], PyQuery)

    assert isinstance(db["data"], str)


def test_data_from_query_processor() -> None:
    test_dict = {"info": {"title": "EasyBook"}}

    db = processors.DataFromQueryProcessor(jp("info")).parse_data(test_dict)

    assert db["data"]["title"] == "EasyBook"


def test_data_from_re_processor() -> None:
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataTextFromReProcessor(
        re_query=r"var config = (.*?);", new_source="config_json"
    )

    db = data_processor.parse_data(test_text)

    assert json.loads(db["config_json"])["title"] == "EasyBook"

    test_text_multiline = """
        var config = {
            "title": "EasyBook"
        };
    """

    db = data_processor.parse_data(test_text_multiline)

    assert json.loads(db["config_json"])["title"] == "EasyBook"


def test_data_from_re_processor_none() -> None:
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataTextFromReProcessor(
        re_query=r"var config_wrong = (.*?);",
        new_source="config_json",
        none_if_empty=True,
    )

    db = data_processor.parse_data(test_text)

    assert db["config_json"] is None


def test_data_from_re_json_processor() -> None:
    test_text = 'var config = {"title": "EasyBook"};'

    data_processor = processors.DataJsonFromReToDictProcessor(
        re_query=r"var config = (.*?);", new_source="config_json"
    )

    db = data_processor.parse_data(test_text)

    assert db["config_json"]["title"] == "EasyBook"


def test_data_variant_processor() -> None:
    db = processors.DataVariantProcessor(
        query=jp("variants"), variant_query=key("color")
    ).parse_data(test_variants_data)

    assert isinstance(db["data_variants"], dict)

    assert len(db["data_variants"]) == 2

    assert list(db["data_variants"].keys())[0] == "black"

    expected_values_result = {"color": "Black", "stock": True}

    assert list(db["data_variants"].values())[0] == expected_values_result


def test_data_variant_processor_multi_values() -> None:
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
        query=pq("#color-variants .color").items, variant_query=pq().text
    ).parse_data(test_variants_html_data)

    assert isinstance(db["data_variants"], dict)

    assert len(db["data_variants"]) == 2

    assert list(db["data_variants"].keys())[0] == "black"


def test_data_variant_processor_lower_false() -> None:
    db = processors.DataVariantProcessor(
        query=key("variants"),
        variant_query=jp("color"),
        variant_values_lower=False,
        multi_values=True,
    ).parse_data(test_variants_data_multi)

    assert list(db["data_variants"].keys())[0] == "Black"


def test_data_variant_processor_with_variant_values_false() -> None:
    db = processors.DataVariantProcessor(
        query=key("variants"),
        variant_query=jp("color"),
        with_variant_values=False,
        multi_values=True,
    ).parse_data(test_variants_data_multi)

    assert isinstance(db["data_variants"], list)

    assert len(db["data_variants"]) == 2

    assert db["data_variants"][0][0]["color"] == "Black"
