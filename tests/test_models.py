from tests.factory.blocks import ItemSettingsBlock, PricingBlock
from tests.factory.models import (
    ProductModel,
    ProductSimpleWithProcessDataModel,
    ProductSimpleWithProcessItemModel,
)

test_html_source = """
    <html>
        <body>
            <h2 class="name">EasyBook Pro 15</h2>
            <div id="price">Was 999.9</div>
            <div id="sale-price">499.9</div>
        </body>
    </html>
"""

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

    item = product_model.parse_item(test_html_source, json_data=test_dict_source)

    assert item == item_model_expected_result


def test_item_model_blocks():
    product_model = ProductModel()
    product_model.blocks = [PricingBlock(), ItemSettingsBlock()]

    item = product_model.parse_item(test_html_source, json_data=test_dict_source)

    item_block_result = {
        "calling_code": 44,
        "country": "UK",
        "price": 999.9,
        "sale_price": 499.9,
        "discount": 50.01,
    }

    item_model_result = item_model_expected_result.copy()

    assert item == {**item_model_result, **item_block_result}


def test_item_model_get_item_attr_names():
    product_model = ProductModel()

    expected_result = ["designer", "language", "name", "stock", "tags", "brand"]
    assert product_model.get_item_attr_names() == expected_result

    product_model.blocks = [ItemSettingsBlock()]

    product_model.parse_item(test_html_source, json_data=test_dict_source)
    expected_result = ["calling_code", "country"] + expected_result
    assert product_model.get_item_attr_names() == expected_result


def test_item_model_process_data():
    """ Here we are testing preprocess_data and process_data methods. """

    test_bad_json_source = '{"brand": "EasyData"'

    product_model = ProductSimpleWithProcessDataModel()
    item = product_model.parse_item(test_bad_json_source)

    assert item == {"brand": "EasyData", "brand_type": "local"}


def test_item_model_process_item():
    """ Here we are testing preprocess_item and process_item methods. """
    test_dict_bad_price_source = {"price": 999.9, "sale_price": 1}

    product_model = ProductSimpleWithProcessItemModel()
    item = product_model.parse_item(test_dict_bad_price_source)

    assert item == {"discount": 0, "final_sale": False, "price": 999.9}
