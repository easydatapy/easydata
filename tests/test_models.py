import json

import pytest

import easydata as ed
from easydata.exceptions import DropItem
from tests.factory import data_dict, data_html
from tests.factory.models import (
    PricingBlockModel,
    ProductHtmlModelWithItems,
    ProductHtmlModelWithVariantItems,
    ProductJsonModelWithComplexVariantItems,
    ProductJsonModelWithMultiItems,
    ProductJsonModelWithVariantDropItems,
    ProductJsonModelWithVariantItems,
    ProductModel,
    SettingsBlockModel,
)

test_dict_source = {"info": {"stock": True}, "brand": "EasyData"}

item_model_expected_result = {
    "designer": "EasyData",
    "language": "en",
    "name": "EasyBook Pro 15",
    "stock": True,
    "tags": ["phones", "ecommerce"],
}


def test_item_model():
    product_model = ProductModel()

    item = product_model.parse_item(
        data_html.prices_and_variants, json_data=test_dict_source
    )

    assert item == item_model_expected_result


def test_item_model_multi():
    product_model = ProductHtmlModelWithItems()

    result_variants = [
        {"color": "Black", "name": "EasyBook Pro 15"},
        {"color": "Gray", "name": "EasyBook Pro 15"},
    ]

    test_data = data_html.prices_and_variants
    assert list(product_model.parse_items(test_data)) == result_variants


def test_item_model_with_variant_items():
    product_model = ProductHtmlModelWithVariantItems()

    result_variants = [
        {"color": "Black", "key": "BLACK", "name": "EasyBook Pro 15"},
        {"color": "Gray", "key": "GRAY", "name": "EasyBook Pro 15"},
    ]

    test_data = data_html.prices_and_variants
    assert list(product_model.parse_items(test_data)) == result_variants


def test_item_model_with_variant_items_multi():
    product_model = ProductJsonModelWithVariantItems()

    result_variants = [
        {
            "color": "Black",
            "key": "BLACK",
            "name": "EasyData Pro",
            "screen_sizes": {"13": True, "15": True},
        },
        {
            "color": "Gray",
            "key": "GRAY",
            "name": "EasyData Pro",
            "screen_sizes": {"13": False, "15": True},
        },
    ]

    test_data = json.dumps(data_dict.variants_data_multi)
    assert list(product_model.parse_items(test_data)) == result_variants


def test_item_model_with_variant_drop_items_multi():
    product_model = ProductJsonModelWithVariantDropItems()

    test_data = json.dumps(data_dict.variants_data_multi)

    with pytest.raises(DropItem) as excinfo:
        list(product_model.parse_items(test_data))

    assert "matched key: black" in str(excinfo.value).lower()


def test_item_model_with_variant_drops_items_multi():
    class TestMultipleDropsModel(ProductJsonModelWithVariantDropItems):
        _item_drop_color = ed.DropContains(
            from_item="color", contains=["black", "gray"]
        )

    product_model = TestMultipleDropsModel()

    test_data = json.dumps(data_dict.variants_data_multi)

    with pytest.raises(DropItem) as excinfo:
        list(product_model.parse_items(test_data))

    exception_msgs = ["matched key: black", "matched key: gray"]

    assert all(em in str(excinfo.value).lower() for em in exception_msgs)


def test_item_model_with_complex_variant_items_multi():
    product_model = ProductJsonModelWithComplexVariantItems()

    result_variants = [
        {
            "color": "Black",
            "images": [
                "https://demo.com/is/image/easydata/33019_B_PRIMARY",
                "https://demo.com/is/image/easydata/33020_B_ALT1",
            ],
            "name": "EasyData Pro",
            "sizes": {"13": True, "15": True},
        },
        {
            "color": "Gray",
            "images": [
                "https://demo.com/is/image/easydata/33021_G_PRIMARY",
                "https://demo.com/is/image/easydata/33022_G_ALT2",
            ],
            "name": "EasyData Pro",
            "sizes": {"13": False, "15": True},
        },
    ]

    test_data = data_dict.variants_data_multi_complex
    assert list(product_model.parse_items(test_data)) == result_variants


def test_item_block_models():
    product_model = ProductModel()
    product_model.block_models = [PricingBlockModel(), SettingsBlockModel()]

    test_data = data_html.prices_and_variants
    item = product_model.parse_item(test_data, json_data=test_dict_source)

    item_block_result = {
        "calling_code": 44,
        "country": "UK",
        "price": 999.9,
        "sale_price": 499.9,
        "discount": 50.01,
    }

    item_model_result = item_model_expected_result.copy()

    assert item == {**item_model_result, **item_block_result}


def test_item_model_as_item_model_value():
    product_model = ProductModel()
    product_model.item_prices = PricingBlockModel()
    product_model.block_models = [SettingsBlockModel()]

    test_data = data_html.prices_and_variants
    item = product_model.parse_item(test_data, json_data=test_dict_source)

    item_block_result = {
        "calling_code": 44,
        "country": "UK",
        "prices": {
            "price": 999.9,
            "sale_price": 499.9,
            "discount": 50.01,
        },
    }

    item_model_result = item_model_expected_result.copy()

    assert item == {**item_model_result, **item_block_result}


def test_item_model_with_multi_items():
    product_model = ProductJsonModelWithMultiItems()

    result_variants = [
        {
            "color": "Black",
            "key": "BLACK",
            "name": "EasyData Pro",
            "screen_sizes": {"13": True, "15": True},
        },
        {
            "color": "Gray",
            "key": "GRAY",
            "name": "EasyData Pro",
            "screen_sizes": {"13": False, "15": True},
        },
        {
            "color": "Black",
            "key": "BLACK",
            "name": "EasyPod",
            "screen_sizes": {"8": True},
        },
        {
            "color": "Gray",
            "key": "GRAY",
            "name": "EasyPod",
            "screen_sizes": {"8": False, "10": True},
        },
    ]

    test_data = data_dict.multi_items
    assert list(product_model.parse_items(test_data)) == result_variants


@pytest.mark.parametrize(
    "test_data, stacked_model, result",
    [
        (
            data_dict.item_with_options,
            ed.StackedModel(
                ed.ItemDiscountProcessor(),
                ED_PRICE_DECIMALS=1,
                name=ed.Text(ed.jp("title")),
                price=ed.PriceFloat(ed.jp("price")),
                _sale_price=ed.PriceFloat(ed.jp("sale_price")),
            ),
            [{"discount": 50.0, "name": "EasyBook pro 15", "price": 100.0}],
        ),
        (
            data_dict.item_with_options,
            ed.StackedModel(
                options=ed.List(
                    query=ed.jp("options"),
                    parser=ed.ItemDict(quantity=ed.Bool(ed.Int(ed.jp("quantity")))),
                ),
            ),
            [
                {
                    "options": [
                        {
                            "quantity": True,
                        },
                        {
                            "quantity": False,
                        },
                    ]
                }
            ],
        ),
        (
            data_dict.variants_data_multi,
            ed.StackedModel(
                ed.DataFromQueryProcessor(ed.jp("data")),
                ed.DataVariantsProcessor(
                    query=ed.jp("variants"),
                    key_parser=ed.Text(ed.jp("color")),
                    new_source="color_data",
                ),
                name=ed.Text(ed.jp("title")),
                color=ed.Text(
                    ed.jp("color"),
                    source="color_data",
                ),
                key=ed.Text(
                    source="color_data_key",
                    uppercase=True,
                ),
                screen_sizes=ed.BoolDict(
                    key_parser=ed.Text(ed.jp("size")),
                    val_query=ed.jp("stock"),
                    source="color_data_variants",
                ),
            ),
            [
                {
                    "color": "Black",
                    "screen_sizes": {"13": True, "15": True},
                    "key": "BLACK",
                    "name": "EasyData Pro",
                },
                {
                    "color": "Gray",
                    "screen_sizes": {"13": False, "15": True},
                    "key": "GRAY",
                    "name": "EasyData Pro",
                },
            ],
        ),
    ],
)
def test_stacked_model(test_data, stacked_model, result):
    assert list(stacked_model.parse_items(test_data)) == result
