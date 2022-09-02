import easydata as ed


class ProductModel(ed.ItemModel):
    item_language = "en"

    item_tags = ["phones", "ecommerce"]

    _item_brand = ed.Text(ed.jp("brand"), source="json_data")

    item_designer = ed.Text(from_item="brand")

    item_name = ed.Text(ed.pq(".name::text"))

    def item_stock(self, data):
        return data["json_data"]["info"]["stock"]


class ProductHtmlModelWithItems(ed.ItemModel):
    data_processors = [
        ed.DataVariantsProcessor(
            query=ed.pq("#color-variants .color::items"), new_source="color_data"
        )
    ]

    item_name = ed.Text(ed.pq(".name::text"))

    item_color = ed.Text(ed.pq(".color-name::text"), source="color_data")


class ProductHtmlModelWithVariantItems(ed.ItemModel):
    data_processors = [
        ed.DataVariantsProcessor(
            query=ed.pq("#color-variants .color::items"),
            key_parser=ed.Text(ed.pq(".color-name::text")),
            new_source="color_data",
        )
    ]

    item_name = ed.Text(ed.pq(".name::text"))

    item_color = ed.Text(ed.pq(".color-name::text"), source="color_data")

    item_key = ed.Text(source="color_data_key", uppercase=True)


class ProductJsonModel(ed.ItemModel):
    item_currency = "USD"

    item_tags = ["notebook", "ecommerce"]

    item_name = ed.Text(ed.jp("title"))

    item_price = ed.PriceFloat(ed.jp("price"))

    item_sale_price = ed.PriceFloat(ed.jp("sale_price"))


class ProductJsonModelWithVariantItems(ed.ItemModel):
    data_processors = [
        ed.DataJsonToDictProcessor(),
        ed.DataFromQueryProcessor(ed.jp("data")),
        ed.DataVariantsProcessor(
            query=ed.jp("variants"),
            key_parser=ed.Text(ed.jp("color")),
            new_source="color_data",
        ),
    ]

    item_name = ed.Text(ed.jp("title"))

    item_color = ed.Text(ed.jp("color", source="color_data"))

    item_key = ed.Text(source="color_data_key", uppercase=True)

    item_screen_sizes = ed.BoolDict(
        key_parser=ed.Text(ed.jp("size")),
        val_query=ed.key("stock"),
        source="color_data_variants",
    )


class ProductJsonModelWithVariantDropItems(ed.ItemModel):
    data_processors = [
        ed.DataJsonToDictProcessor(),
        ed.DataFromQueryProcessor(ed.jp("data")),
        ed.DataVariantsProcessor(
            query=ed.jp("variants"),
            key_parser=ed.Text(ed.jp("color")),
            new_source="color_data",
        ),
    ]

    _item_drop_color = ed.DropContains(from_item="color", contains=["black"])

    item_color = ed.Text(ed.jp("color", source="color_data"))


class ProductJsonModelWithComplexVariantItems(ed.ItemModel):
    data_processors = [
        ed.DataVariantsProcessor(
            query=ed.jp("variants"),
            key_parser=ed.Text(ed.jp("color")),
            new_source="color_data",
        )
    ]

    item_name = ed.Text(ed.jp("title"))

    item_color = ed.Text(ed.jp("color"), source="color_data")

    item_images = ed.UrlList(
        ed.jp(
            "images.{color}[].assetId",
            params={"color": ed.Data(ed.jp("color"), source="color_data")},
        ),
        domain="https://demo.com/is/image/easydata/",
    )

    item_sizes = ed.Dict(
        source="color_data_variants",
        key_parser=ed.Text(ed.jp("size")),
        val_parser=ed.Bool(
            ed.jp(
                "stock_data[?id==`{stock_id}`] | [0].stock",
                params={"stock_id": ed.SearchInt(ed.jp("stock_id"))},
            ),
            source="main",
        ),
    )


class ProductJsonModelWithMultiItems(ed.ItemModel):
    data_processors = [
        ed.DataFromQueryProcessor(ed.jp("data")),
        ed.DataFromIterQueryProcessor(ed.jp("items")),
        ed.DataVariantsProcessor(
            query=ed.jp("variants"),
            key_parser=ed.Text(ed.jp("color")),
            new_source="color_data",
        ),
    ]

    item_name = ed.Text(ed.jp("title"))

    item_color = ed.Text(ed.jp("color"), source="color_data")

    item_key = ed.Text(source="color_data_key", uppercase=True)

    item_screen_sizes = ed.BoolDict(
        key_parser=ed.Text(ed.jp("size")),
        val_query=ed.jp("stock"),
        source="color_data_variants",
    )


class ProductSimpleWithProcessDataModel(ed.ItemModel):
    data_processors = [ed.DataJsonToDictProcessor()]

    item_brand = ed.Text(ed.jp("brand"))

    item_brand_type = ed.Text(source="brand_type")

    def preprocess_data(self, data):
        data["main"] = data["main"] + "}"

        return data

    def process_data(self, data):
        if "easydata" in data["main"]["brand"].lower():
            data["brand_type"] = "local"
        else:
            data["brand_type"] = "other"

        return data


class ProductSimpleWithProcessItemModel(ed.ItemModel):
    item_price = ed.PriceFloat(ed.jp("price"))

    _item_sale_price = ed.PriceFloat(ed.jp("sale_price"))

    item_processors = [ed.ItemDiscountProcessor()]

    def preprocess_item(self, item):
        if item["sale_price"] <= 1:
            item["sale_price"] = 0

        return item

    def process_item(self, item):
        item["final_sale"] = bool(item["discount"])

        return item


class PricingBlockModel(ed.ItemModel):
    item_price = ed.PriceFloat(ed.pq("#price::text"))

    item_sale_price = ed.PriceFloat(ed.pq("#sale-price::text"))

    item_processors = [("discount", ed.ItemDiscountProcessor())]


class SettingsBlockModel(ed.ItemModel):
    item_calling_code = 44

    item_country = "UK"
