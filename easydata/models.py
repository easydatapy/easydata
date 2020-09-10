from abc import ABC
from typing import Any, List, Optional

from easydata.data import DataBag
from easydata.managers import ModelManager
from easydata.processors.base import BaseProcessor
from easydata.processors.data import DataBaseProcessor

__all__ = ("ItemModel",)


class BaseModel(ABC):
    block_models: List[Any] = []

    data_processors: List[DataBaseProcessor] = []

    items_processors: List[BaseProcessor] = []

    _model_manager: Optional[ModelManager] = None

    def preprocess_data(self, data: DataBag):
        return data

    def process_data(self, data: DataBag):
        return data

    def preprocess_item(self, item: dict):
        return item

    def process_item(self, item: dict):
        return item

    @property
    def model_manager(self):
        if not self._model_manager:
            self._model_manager = ModelManager(self)

        return self._model_manager

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
