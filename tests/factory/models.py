from easydata import ItemModel, parsers, processors
from easydata.queries import jp, key, pq


class ProductModel(ItemModel):
    item_language = "en"

    item_tags = ["phones", "ecommerce"]

    _item_brand = parsers.Text(jp("brand"), source="json_data")

    item_designer = parsers.Text(from_item="brand")

    item_name = parsers.Text(pq(".name::text"))

    def item_stock(self, data):
        return data["json_data"]["info"]["stock"]


class ProductHtmlModelWithItems(ItemModel):
    with_items = True

    data_processors = [
        processors.DataFromQueryProcessor(
            pq("#color-variants .color::items"), new_source="variant"
        )
    ]

    item_name = parsers.Text(pq(".name::text"))

    items_source = "variant"

    item_color = parsers.Text(pq(".color-name::text"), source="variant")


class ProductHtmlModelWithVariantItems(ItemModel):
    with_items = True

    data_processors = [
        processors.DataVariantsProcessor(
            query=pq("#color-variants .color::items"),
            key_parser=parsers.Text(pq(".color-name::text")),
        )
    ]

    item_name = parsers.Text(pq(".name::text"))

    item_color = parsers.Text(pq(".color-name::text"), source="variant_data")

    item_key = parsers.Text(source="variant_key", uppercase=True)


class ProductJsonModelWithVariantItemsMulti(ItemModel):
    with_items = True

    data_processors = [
        processors.DataVariantsProcessor(
            query=jp("variants"), key_parser=parsers.Text(jp("color"))
        )
    ]

    item_name = parsers.Text(jp("title"))

    item_color = parsers.Text(jp("color"), source="variant_data")

    item_key = parsers.Text(source="variant_key", uppercase=True)

    item_screen_sizes = parsers.BoolDict(
        key_parser=parsers.Text(jp("size")),
        val_query=key("stock"),
        source="variants",
    )


class ProductSimpleWithProcessDataModel(ItemModel):
    item_brand = parsers.Text(jp("brand"))

    item_brand_type = parsers.Text(source="brand_type")

    data_processors = [processors.DataJsonToDictProcessor()]

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

    _item_sale_price = parsers.PriceFloat(jp("sale_price"))

    item_processors = [processors.ItemDiscountProcessor()]

    def preprocess_item(self, item):
        if item["sale_price"] <= 1:
            item["sale_price"] = 0

        return item

    def process_item(self, item):
        item["final_sale"] = bool(item["discount"])

        return item


class PricingBlockModel(ItemModel):
    item_price = parsers.PriceFloat(pq("#price::text"))

    item_sale_price = parsers.PriceFloat(pq("#sale-price::text"))

    item_processors = [("discount", processors.ItemDiscountProcessor())]


class SettingsBlockModel(ItemModel):
    item_calling_code = 44

    item_country = "UK"
