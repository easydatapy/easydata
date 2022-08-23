from abc import ABC
from functools import cached_property
from typing import Optional

from scrapy import Spider
from scrapy.http import Response
from scrapy.spiders import CrawlSpider

from easydata.contrib.scrapy.models import ItemModel

__all__ = (
    "ItemModelSpider",
    "ItemModelCrawlSpider",
)


class ItemModelMixin:
    item_model_cls = None

    item_model_obj: Optional[ItemModel] = None

    def parse_item_model(
        self,
        response: Optional[Response] = None,
        **cb_kwargs,
    ):

        return self.item_model_instance.parse_res2items(
            response,
            **cb_kwargs,
        )

    @cached_property
    def item_model_instance(self) -> ItemModel:
        item_model_cls = getattr(self, "ItemModel", None)

        if item_model_cls:
            return self.init_item_model_obj(item_model_cls)
        elif self.item_model_cls:
            return self.init_item_model_obj(self.item_model_cls)
        elif self.item_model_obj:
            return self.item_model_obj

        error_msg = "ItemModel can be implemented through item_model_cls or inner class"

        raise NotImplementedError(error_msg)

    def init_item_model_obj(self, item_model_cls):
        """Override this method in order to pass parameters to __init__ in item model"""
        return item_model_cls()


class ItemModelSpider(ItemModelMixin, Spider, ABC):
    pass


class ItemModelCrawlSpider(ItemModelMixin, CrawlSpider, ABC):
    pass
