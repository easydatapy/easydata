from abc import ABC
from functools import lru_cache
from typing import Iterator

from easydata.data import DataBag
from easydata.managers import ModelManager
from easydata.processors.data import DataBaseProcessor
from easydata.processors.item import ItemBaseProcessor

__all__ = (
    "BaseModel",
    "ItemModel",
    "StackedMixin",
    "StackedModel",
)


class BaseModel(ABC):
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

        yield from self.model_manager.parse_data_to_items(data, **kwargs)


class ItemModel(BaseModel):
    def parse_items(
        self,
        data=None,
        **kwargs,
    ) -> Iterator[dict]:

        yield from self._parse_items(data, **kwargs)

    def parse_item(
        self,
        data=None,
        **kwargs,
    ) -> dict:

        return next(self._parse_items(data, **kwargs))


class StackedMixin:
    def __init__(self, *components, **item_components):

        self.block_models = []

        self.data_processors = []

        self.item_processors = []

        self._initialize_components(components)

        self._initialize_item_components(item_components)

    def _initialize_components(self, components):
        for component in components:
            if isinstance(component, ItemModel):
                self.block_models.append(component)
            elif isinstance(component, DataBaseProcessor):
                self.data_processors.append(component)
            elif isinstance(component, ItemBaseProcessor):
                self.item_processors.append(component)
            else:
                raise TypeError(
                    "Unknown components. Supported are only item processors, data "
                    "processors and item block models"
                )

    def _initialize_item_components(self, item_components):
        for item_name, item_component in item_components.items():
            if item_name.startswith("ED_"):
                setattr(self, item_name, item_component)
            elif item_name[0] == "_":
                setattr(self, "_item{}".format(item_name), item_component)
            else:
                setattr(self, "item_{}".format(item_name), item_component)


class StackedModel(StackedMixin, ItemModel):
    pass
