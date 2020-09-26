import json

import pytest

from easydata import parsers, processors
from easydata.models import StackedModel
from easydata.queries import jp
from tests.factory import data_dict, data_html
from tests.factory.models import (
    PricingBlockModel,
    ProductHtmlModelWithItems,
    ProductHtmlModelWithVariantItems,
    ProductJsonModelWithComplexVariantItems,
    ProductJsonModelWithMultiItems,
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
            StackedModel(
                processors.ItemDiscountProcessor(),
                ED_PRICE_DECIMALS=1,
                name=parsers.Text(jp("title")),
                price=parsers.PriceFloat(jp("price")),
                _sale_price=parsers.PriceFloat(jp("sale_price")),
            ),
            [{"discount": 50.0, "name": "EasyBook pro 15", "price": 100.0}],
        ),
        (
            data_dict.variants_data_multi,
            StackedModel(
                processors.DataFromQueryProcessor(jp("data")),
                processors.DataVariantsProcessor(
                    query=jp("variants"),
                    key_parser=parsers.Text(jp("color")),
                    new_source="color_data",
                ),
                name=parsers.Text(jp("title")),
                color=parsers.Text(
                    jp("color"),
                    source="color_data",
                ),
                key=parsers.Text(
                    source="color_data_key",
                    uppercase=True,
                ),
                screen_sizes=parsers.BoolDict(
                    key_parser=parsers.Text(jp("size")),
                    val_query=jp("stock"),
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
