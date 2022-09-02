import pytest

import easydata as ed
from easydata.data import DataBag
from tests.factory import data_dict, data_html


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("EasyWATCH", "watch"),
        ("EasyBook mon 15", "notebook"),
        ("EasyLCD 22", "monitor"),
        ("EasyOS 2020", "software"),
        ("EasyPhone 12", "phone"),
        ("EasyPhone case 12", "accessory"),
        ("EasyMonitor 22", "monitor"),
    ],
)
def test_choice_choices(test_data, result):
    choice_parser = ed.Choice(
        choices=[
            ("accessory", ["phone case"]),
            ("watch", "watch"),
            ("monitor", ed.Bool(ccontains=["LCD"])),
            ("notebook", [r"book\b"]),
            (
                "phone",
                (
                    "mobile",
                    "phone",
                ),
            ),
            ("monitor", ["oled", "monitor"]),
        ],
        default_choice="software",
    )
    assert choice_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "pq_query, bool_query, result",
    [
        ("#accessory .name::text", "name", "phone"),
        ("#accessory .name::text", "title", "accessory"),
        ("#accessory .title::text", "title", None),
    ],
)
def test_choice_lookup_queries_choice_bool_parser_source(
    pq_query,
    bool_query,
    result,
):
    def generate_choice_parser(**kwargs):
        return ed.Choice(
            choices=[
                (
                    "phone",
                    ed.Bool(
                        query=ed.jp(bool_query),
                        ccontains=["phone", "CELL"],
                        source="json_data",
                    ),
                ),
                ("accessory", ["phone"]),
            ],
            **kwargs
        )

    data_bag = DataBag(main=data_html.categories, json_data=data_dict.name)

    # Test lookup queries
    choice_parser = generate_choice_parser(lookups=[ed.pq(pq_query)])

    assert choice_parser.parse(data_bag) == result

    # Test lookup parsers
    choice_parser = generate_choice_parser(lookups=[ed.Text(ed.pq(pq_query))])

    assert choice_parser.parse(data_bag) == result


def test_choice_lookup_items():
    class ProductModel(ed.ItemModel):
        _item_category = ed.Text(ed.pq("#accessory .name::text"))

        _item_name = ed.Text(ed.pq("#accessory .type::text"))

        item_type = ed.Choice(
            lookups=["name", "category"],
            choices=[
                ("phone", ["mobile"]),
                ("accessory", ["phone case"]),
            ],
        )

    assert ProductModel().parse_item(data_html.categories) == {"type": "accessory"}
