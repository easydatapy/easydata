from typing import Optional

from scrapy import Field, Item
from scrapy.http import Request, TextResponse

import easydata as ed
from easydata.contrib.scrapy.models import ItemModel, StackedModel
from tests.factory import data_dict


def fake_response(
    url: str = "https://demo.com/test",
    body: str = data_dict.item_with_options_text,
    meta: Optional[dict] = None,
    encoding: str = "utf-8",
    cb_kwargs: Optional[dict] = None,
):

    request = Request(
        url=url,
        encoding=encoding,
        meta=meta,
        cb_kwargs=cb_kwargs,
    )

    return TextResponse(
        url=url,
        body=body,
        encoding=encoding,
        request=request,
    )


class ProductItem(Item):
    name = Field()
    brand = Field()
    url = Field()


class ProductItemModel(ItemModel):
    data_processors = [
        ed.DataJsonToDictProcessor(),
    ]

    item_name = ed.Text(ed.jp("title"))
    item_brand = ed.Text(ed.jp("brand.name"))
    item_url = ed.Url(source="url")


PRODUCT_ITEM_STACKED_MODEL = StackedModel(
    data_processors=[
        ed.DataJsonToDictProcessor(),
    ],
    name=ed.Text(ed.jp("title")),
    brand=ed.Text(ed.jp("brand.name")),
    url=ed.Url(source="url"),
)


EXPECTED_PRODUCT_ITEM_RESULT = {
    "brand": "EasyData",
    "name": "EasyBook pro 15",
    "url": "https://demo.com/test",
}

EXPECTED_PRODUCT_ITEM_RESULT_SCRAPY_ITEM = ProductItem(**EXPECTED_PRODUCT_ITEM_RESULT)
