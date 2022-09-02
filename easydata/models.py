from abc import ABC
from functools import lru_cache
from typing import Any, Callable, Iterator, List, Optional

from easydata.managers import ModelManager
from easydata.parsers.base import Base
from easydata.processors.data import DataBaseProcessor
from easydata.processors.item import ItemBaseProcessor

__all__ = (
    "BaseModel",
    "ItemModel",
    "StackedMixin",
    "StackedModel",
    "StackedParser",
)


class BaseModel(ABC):
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
    def __init__(
        self,
        *args,
        block_models: Optional[List[BaseModel]] = None,
        data_processors: Optional[List[DataBaseProcessor]] = None,
        item_processors: Optional[List[ItemBaseProcessor]] = None,
        preprocess_data: Optional[Callable] = None,
        process_data: Optional[Callable] = None,
        preprocess_item: Optional[Callable] = None,
        process_item: Optional[Callable] = None,
        init_model: Optional[Callable] = None,
        initialized_model: Optional[Callable] = None,
        **kwargs,
    ):

        self.block_models: List[BaseModel] = []
        self.data_processors: List[DataBaseProcessor] = []
        self.item_processors: List[ItemBaseProcessor] = []

        if block_models:
            if not isinstance(block_models, list):
                raise TypeError("block_models must be of type list")

            self.block_models = block_models

        if data_processors:
            if not isinstance(data_processors, list):
                raise TypeError("data_processors must be of type list")

            self.data_processors = data_processors

        if item_processors:
            if not isinstance(item_processors, list):
                raise TypeError("item_processors must be of type list")

            self.item_processors = item_processors

        if preprocess_data:
            self.preprocess_data = preprocess_data

        if process_data:
            self.process_data = process_data

        if preprocess_item:
            self.preprocess_item = preprocess_item

        if process_item:
            self.process_item = process_item

        if init_model:
            self.init_model = init_model

        if initialized_model:
            self.initialized_model = initialized_model

        self.__initialize_args(args)

        self.__initialize_kwargs(kwargs)

    def __initialize_args(self, args: Any):
        for component in args:
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

    def __initialize_kwargs(self, kwargs):
        for item_name, item_component in kwargs.items():
            if item_name.startswith("ED_"):
                setattr(self, item_name, item_component)
            elif item_name[0] == "_":
                setattr(self, "_item{}".format(item_name), item_component)
            else:
                setattr(self, "item_{}".format(item_name), item_component)


class StackedModel(StackedMixin, ItemModel):
    pass


class StackedParser(StackedModel, Base):
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parent_data = parent_data if with_parent_data else data

        return self.parse_item(
            data=parent_data,
            parent_data=data,
        )
