import requests
from requests_mock import Mocker

import easydata as ed
from easydata.contrib.requests.models import ItemModel, StackedModel
from tests.factory import data_dict


def fake_response(
    url: str = "https://demo.com/test",
    text: str = data_dict.item_with_options_text,
):

    with Mocker() as m:
        m.get(url, text=text)

        response = requests.get(url)

    return response


class ProductItemModel(ItemModel):
    def __init__(self, to_json: bool = True):
        if to_json:
            self.data_processors = [
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
