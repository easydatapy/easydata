from abc import ABC
from functools import lru_cache
from typing import Any, List

from easydata.data import DataBag
from easydata.managers import ModelManager
from easydata.processors.base import BaseProcessor
from easydata.processors.data import DataBaseProcessor


class BaseModel(ABC):
    block_models: List[Any] = []

    data_processors: List[DataBaseProcessor] = []

    item_processors: List[BaseProcessor] = []

    def preprocess_data(self, data: DataBag):
        return data

    def process_data(self, data: DataBag):
        return data

    def preprocess_item(self, item: dict):
        return item

    def process_item(self, item: dict):
        return item

    def init_model(self):
        pass

    def initialized_model(self):
        pass

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def model_manager(self) -> ModelManager:
        return ModelManager(self)

    def _parse_items(
        self,
        data=None,
        **kwargs,
    ):

        return self.model_manager.parse_data_to_items(data, **kwargs)


class ItemModel(BaseModel):
    def iter_parse(
        self,
        data=None,
        **kwargs,
    ) -> dict:

        return self._parse_items(data, **kwargs)

    def parse(
        self,
        data=None,
        **kwargs,
    ) -> dict:

        return next(self._parse_items(data, **kwargs))
