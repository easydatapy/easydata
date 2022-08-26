from typing import Optional

from scrapy.http.response import Response

from easydata.contrib.scrapy.utils import response_to_data_bag
from easydata.models import ItemModel as BaseItemModel
from easydata.models import StackedMixin

__all__ = (
    "ItemModel",
    "StackedModel",
)


class ItemModel(BaseItemModel):
    def parse_res2item(
        self,
        response: Optional[Response] = None,
        to_json: bool = False,
        **cb_kwargs,
    ):

        return next(
            self.parse_res2items(
                response=response,
                to_json=to_json,
                **cb_kwargs,
            )
        )

    def parse_res2items(
        self,
        response: Optional[Response] = None,
        to_json: bool = False,
        **cb_kwargs,
    ):

        if response:
            data_bag = response_to_data_bag(
                response,
                to_json=to_json,
                **cb_kwargs,
            )

            iter_items = super().parse_items(data=data_bag)
        else:
            iter_items = super().parse_items(**cb_kwargs)

        for item in iter_items:
            process_response_item = getattr(self, "process_response_item", None)

            if process_response_item:
                item = process_response_item(item, response, **cb_kwargs)

            scrapy_item_cls = getattr(self, "scrapy_item_cls", None)

            # Create scrapy item object if scrapy item class is set in a spider
            yield scrapy_item_cls(item) if scrapy_item_cls else item


class StackedModel(StackedMixin, ItemModel):
    def __init__(
        self,
        *components,
        scrapy_item_cls=None,
        **item_components,
    ):

        if scrapy_item_cls:
            setattr(self, "scrapy_item_cls", scrapy_item_cls)

        super().__init__(*components, **item_components)
