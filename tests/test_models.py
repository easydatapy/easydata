from tests.factory.models import PricingBlockModel, ProductModel, SettingsBlockModel

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

    item = product_model.parse(test_html_source, json_data=test_dict_source)

    assert item == item_model_expected_result


def test_item_model_blocks():
    product_model = ProductModel()
    product_model.model_blocks = [PricingBlockModel(), SettingsBlockModel()]

    item = product_model.parse(test_html_source, json_data=test_dict_source)

    item_block_result = {
        "calling_code": 44,
        "country": "UK",
        "price": 999.9,
        "sale_price": 499.9,
        "discount": 50.01,
    }

    item_model_result = item_model_expected_result.copy()

    assert item == {**item_model_result, **item_block_result}
