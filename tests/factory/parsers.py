from easydata import parsers
from easydata.models import ItemModel
from easydata.queries import jp, key
from tests.factory import load_json


class SimpleJsonItemModel(ItemModel):
    item_currency = "USD"

    item_tags = ["phones", "ecommerce"]

    item_parser_id = 123

    item_parser_float_id = 123.123

    item_params = {"currency": "USD"}

    item_name = parsers.Text(jp("info.name"))

    item_brand = parsers.Text(jp("info.brand"))

    item_product_type = parsers.Text(key("product_type"))

    item_image_urls = parsers.List(jp("images[*].zoom"), parsers.Url(normalize=True))

    def extract_data(self):
        json_data = load_json("product")

        return self.parse_item(json_data)
