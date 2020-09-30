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
    data_processors = [
        processors.DataVariantsProcessor(
            query=pq("#color-variants .color::items"), new_source="color_data"
        )
    ]

    item_name = parsers.Text(pq(".name::text"))

    item_color = parsers.Text(pq(".color-name::text"), source="color_data")


class ProductHtmlModelWithVariantItems(ItemModel):
    data_processors = [
        processors.DataVariantsProcessor(
            query=pq("#color-variants .color::items"),
            key_parser=parsers.Text(pq(".color-name::text")),
            new_source="color_data",
        )
    ]

    item_name = parsers.Text(pq(".name::text"))

    item_color = parsers.Text(pq(".color-name::text"), source="color_data")

    item_key = parsers.Text(source="color_data_key", uppercase=True)


class ProductJsonModel(ItemModel):
    item_currency = "USD"

    item_tags = ["notebook", "ecommerce"]

    item_name = parsers.Text(jp("title"))

    item_price = parsers.PriceFloat(jp("price"))

    item_sale_price = parsers.PriceFloat(jp("sale_price"))


class ProductJsonModelWithVariantItems(ItemModel):
    data_processors = [
        processors.DataJsonToDictProcessor(),
        processors.DataFromQueryProcessor(jp("data")),
        processors.DataVariantsProcessor(
            query=jp("variants"),
            key_parser=parsers.Text(jp("color")),
            new_source="color_data",
        ),
    ]

    item_name = parsers.Text(jp("title"))

    item_color = parsers.Text(jp("color"), source="color_data")

    item_key = parsers.Text(source="color_data_key", uppercase=True)

    item_screen_sizes = parsers.BoolDict(
        key_parser=parsers.Text(jp("size")),
        val_query=key("stock"),
        source="color_data_variants",
    )


class ProductJsonModelWithVariantDropItems(ItemModel):
    data_processors = [
        processors.DataJsonToDictProcessor(),
        processors.DataFromQueryProcessor(jp("data")),
        processors.DataVariantsProcessor(
            query=jp("variants"),
            key_parser=parsers.Text(jp("color")),
            new_source="color_data",
        ),
    ]

    _item_drop_color = parsers.DropContains(from_item="color", contains=["black"])

    item_color = parsers.Text(jp("color"), source="color_data")


class ProductJsonModelWithComplexVariantItems(ItemModel):
    data_processors = [
        processors.DataVariantsProcessor(
            query=jp("variants"),
            key_parser=parsers.Text(jp("color")),
            new_source="color_data",
        )
    ]

    item_name = parsers.Text(jp("title"))

    item_color = parsers.Text(jp("color"), source="color_data")

    item_images = parsers.UrlList(
        jp("images.{color}[].assetId"),
        query_params={"color": parsers.Data(jp("color"), source="color_data")},
        domain="https://demo.com/is/image/easydata/",
    )

    item_sizes = parsers.Dict(
        source="color_data_variants",
        key_parser=parsers.Text(jp("size")),
        val_parser=parsers.Bool(
            jp("stock_data[?id==`{stock_id}`] | [0].stock"),
            query_params={"stock_id": parsers.Int(jp("stock_id"))},
            source="main",
        ),
    )


class ProductJsonModelWithMultiItems(ItemModel):
    data_processors = [
        processors.DataFromQueryProcessor(jp("data")),
        processors.DataFromIterQueryProcessor(jp("items")),
        processors.DataVariantsProcessor(
            query=jp("variants"),
            key_parser=parsers.Text(jp("color")),
            new_source="color_data",
        ),
    ]

    item_name = parsers.Text(jp("title"))

    item_color = parsers.Text(jp("color"), source="color_data")

    item_key = parsers.Text(source="color_data_key", uppercase=True)

    item_screen_sizes = parsers.BoolDict(
        key_parser=parsers.Text(jp("size")),
        val_query=jp("stock"),
        source="color_data_variants",
    )


class ProductSimpleWithProcessDataModel(ItemModel):
    data_processors = [processors.DataJsonToDictProcessor()]

    item_brand = parsers.Text(jp("brand"))

    item_brand_type = parsers.Text(source="brand_type")

    def preprocess_data(self, data):
        data["main"] = data["main"] + "}"

        return data

    def process_data(self, data):
        if "easydata" in data["main"]["brand"].lower():
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
