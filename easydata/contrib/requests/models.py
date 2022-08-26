from typing import Optional

from requests import Response

from easydata.contrib.requests.utils import response_to_data_bag
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

            yield item


class StackedModel(StackedMixin, ItemModel):
    pass
