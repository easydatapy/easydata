from abc import ABC
from typing import List, Optional

from easydata.data import DataBag
from easydata.models import ItemModel
from easydata.processors.base import BaseProcessor
from easydata.processors.data import DataBaseProcessor

__all__ = ("Block",)


class Block(ABC):
    __cached_model: Optional[ItemModel] = None

    data_processors: List[DataBaseProcessor] = []

    items_processors: List[BaseProcessor] = []

    def preprocess_data(self, data: DataBag):
        return data

    def process_data(self, data: DataBag):
        return data

    def preprocess_item(self, item: dict):
        return item

    def process_item(self, item: dict):
        return item

    def parse_item(self, data, **kwargs):

        if not self.__cached_model:
            self.__cached_model = ItemModel()
            self.__cached_model.blocks = [self]

        return self.__cached_model.parse_item(data, **kwargs)
