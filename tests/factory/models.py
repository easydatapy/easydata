from easydata import parsers
from easydata.models import ItemModel
from easydata.processors import DataJsonToDictProcessor, ItemDiscountProcessor
from easydata.queries import jp, pq


class ProductModel(ItemModel):
    item_language = "en"

    item_tags = ["phones", "ecommerce"]

    item_temp_brand = parsers.Text(jp("brand"), source="json_data")

    item_designer = parsers.Text(from_item="brand")

    item_name = parsers.Text(pq(".name").text)

    def item_stock(self, data):
        return data["json_data"]["info"]["stock"]


class ProductSimpleWithProcessDataModel(ItemModel):
    item_brand = parsers.Text(jp("brand"))

    item_brand_type = parsers.Text(source="brand_type")

    data_processors = [DataJsonToDictProcessor()]

    def preprocess_data(self, data):
        data["data"] = data["data"] + "}"
        return data

    def process_data(self, data):
        if "easydata" in data["data"]["brand"].lower():
            data["brand_type"] = "local"
        else:
            data["brand_type"] = "other"

        return data


class ProductSimpleWithProcessItemModel(ItemModel):
    item_price = parsers.PriceFloat(jp("price"))

    item_temp_sale_price = parsers.PriceFloat(jp("sale_price"))

    items_processors = [ItemDiscountProcessor()]

    def preprocess_item(self, item):
        if item["sale_price"] <= 1:
            item["sale_price"] = 0

        return item

    def process_item(self, item):
        item["final_sale"] = bool(item["discount"])

        return item
