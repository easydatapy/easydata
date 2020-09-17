from tests.factory import dict_data, html_data
from tests.factory.models import (
    PricingBlockModel,
    ProductHtmlModelWithItems,
    ProductHtmlModelWithVariantItems,
    ProductJsonModelWithVariantItemsMulti,
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

    item = product_model.parse(
        html_data.with_prices_and_variants, json_data=test_dict_source
    )

    assert item == item_model_expected_result


def test_item_model_with_items():
    product_model = ProductHtmlModelWithItems()

    result_variants = [
        {"color": "Black", "name": "EasyBook Pro 15"},
        {"color": "Gray", "name": "EasyBook Pro 15"},
    ]

    test_data = html_data.with_prices_and_variants
    assert list(product_model.iter_parse(test_data)) == result_variants


def test_item_model_with_variant_items():
    product_model = ProductHtmlModelWithVariantItems()

    result_variants = [
        {"color": "Black", "key": "BLACK", "name": "EasyBook Pro 15"},
        {"color": "Gray", "key": "GRAY", "name": "EasyBook Pro 15"},
    ]

    test_data = html_data.with_prices_and_variants
    assert list(product_model.iter_parse(test_data)) == result_variants


def test_item_model_with_variant_items_multi():
    product_model = ProductJsonModelWithVariantItemsMulti()

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

    test_data = dict_data.with_variants_data_multi
    assert list(product_model.iter_parse(test_data)) == result_variants


def test_item_block_models():
    product_model = ProductModel()
    product_model.block_models = [PricingBlockModel(), SettingsBlockModel()]

    test_data = html_data.with_prices_and_variants
    item = product_model.parse(test_data, json_data=test_dict_source)

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

    test_data = html_data.with_prices_and_variants
    item = product_model.parse(test_data, json_data=test_dict_source)

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
