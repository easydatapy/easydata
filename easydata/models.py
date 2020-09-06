from abc import ABC, abstractmethod
from typing import Any, List

from easydata import config, parsers
from easydata.data import DataBag
from easydata.managers import ObjectManager
from easydata.mixins import ConfigMixin
from easydata.parsers.base import Base
from easydata.processors.base import BaseProcessor
from easydata.processors.data import DataBaseProcessor
from easydata.utils import mix

__all__ = ("ItemModel",)


class BaseModel(ConfigMixin, ABC):
    @abstractmethod
    def parse_item(self, data) -> dict:
        pass

    @abstractmethod
    def parse_items(self, data):
        pass

    @abstractmethod
    def parse_item_properties(
        self,
        item_name: str,
        data: DataBag,
    ):

        pass

    @abstractmethod
    def get_item_attr_names(self):
        pass

    @property
    def config(self):
        if not self._config:
            self._config = config.copy()

        return self._config


class ItemModel(BaseModel):
    blocks: List[Any] = []

    data_processors: List[DataBaseProcessor] = []

    data_variants_name: str = "variants"

    data_variant_name: str = "variant"

    data_variants_key_name: str = "variants_key"

    items_processors: List[BaseProcessor] = []

    items_split_by_variants: bool = False

    _model_initialized: bool = False

    _cached_item_names: List[str] = []

    _cached_item_temp_names: List[str] = []

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

    def parse_item(
        self,
        data=None,
        **kwargs,
    ) -> dict:

        return next(self.parse_items(data, **kwargs))

    def parse_items(
        self,
        data=None,
        **kwargs,
    ):

        self._init_model()

        if data:
            kwargs["data"] = data

        data = DataBag(self, **kwargs)

        data = self._apply_data_processors(data)

        if self.items_split_by_variants:
            for variant_data in self._parse_variants_data(data):
                item = variant_data.get_multi(self.get_item_attr_names())

                item = self._apply_items_processors(item)

                yield self._remove_temp_item_keys(item)
        else:
            item = data.get_multi(self.get_item_attr_names())

            item = self._apply_items_processors(item)

            yield self._remove_temp_item_keys(item)

    def parse_item_properties(self, item_name: str, data: DataBag):
        if item_name in self._cached_item_temp_names:
            attr_item_name = "item_temp_{}".format(item_name)
        else:
            attr_item_name = "item_{}".format(item_name)

        item_field = getattr(self, attr_item_name)

        if isinstance(item_field, (str, float, int, list, dict)):
            return item_field
        elif isinstance(item_field, parsers.Base):
            return item_field.parse(data)

        return item_field(data)

    def get_item_attr_names(self) -> list:
        if self._cached_item_names:
            return self._cached_item_names

        for attr_item_name in mix.extract_item_attr_names_from_cls(self):
            if attr_item_name.startswith("temp_"):
                attr_item_name = attr_item_name.replace("temp_", "")

                self._cached_item_temp_names.append(attr_item_name)

            self._cached_item_names.append(attr_item_name)

        return self._cached_item_names

    def _init_model(self):
        if not self._model_initialized:
            self._cached_item_names = []

            self._cached_item_temp_names = []

            self._data_processors_manager = ObjectManager()

            self._items_processors_manager = ObjectManager()

            self._init_blocks()

            self.config.from_module(self)

            self._init_item_parsers()

            self._init_data_processors()

            self._init_items_processors()

            self.init_model()

            self._model_initialized = True

    def _init_item_parsers(self):
        for item_name in mix.extract_item_attr_names_from_cls(self):
            item_parser = getattr(self, "item_{}".format(item_name))

            if isinstance(item_parser, Base):
                item_parser.init_config(self.config)

    def _init_blocks(self):
        for block in self.blocks:
            self.config.from_module(block)

            if block.data_processors:
                self._data_processors_manager.add_list(block.data_processors)

            if block.items_processors:
                self._items_processors_manager.add_list(block.items_processors)

            for block_attr_data in mix.iter_item_attr_data_from_cls(block):
                item_attr_name, item_attr_value = block_attr_data

                if not hasattr(self, item_attr_name):
                    setattr(self, item_attr_name, item_attr_value)

    def _init_data_processors(self):
        if self.data_processors:
            self._data_processors_manager.add_list(self.data_processors)

    def _init_items_processors(self):
        if self.items_processors:
            self._items_processors_manager.add_list(self.items_processors)

    def _parse_variants_data(self, data):
        variants_data = data[self.items_split_by_variants]

        if isinstance(variants_data, dict):
            for variant_key, variant_data in variants_data.items():
                yield mix.make_variant_data_copy(
                    data=data,
                    variant_data=variant_data,
                    variant_key=variant_key,
                    variants_name=self.data_variants_name,
                    variant_name=self.data_variant_name,
                    variants_key_name=self.data_variants_key_name,
                )
        else:
            for variant_data in variants_data:
                yield mix.make_variant_data_copy(
                    data=data,
                    variant_data=variant_data,
                    variants_name=self.data_variants_name,
                    variant_name=self.data_variant_name,
                    variants_key_name=self.data_variants_key_name,
                )

    def _apply_data_processors(self, data: DataBag) -> DataBag:
        for block in self.blocks:
            data = block.preprocess_data(data)

        data = self.preprocess_data(data)

        data = mix.apply_processors(
            value=data,
            processors=list(self._data_processors_manager.values()),
        )

        for block in self.blocks:
            data = block.process_data(data)

        return self.process_data(data)

    def _apply_items_processors(self, item: dict) -> dict:
        for block in self.blocks:
            item = block.preprocess_item(item)

        item = self.preprocess_item(item)

        item = mix.apply_processors(
            value=item,
            processors=list(self._items_processors_manager.values()),
        )

        for block in self.blocks:
            item = block.process_item(item)

        return self.process_item(item)

    def _remove_temp_item_keys(self, item: dict) -> dict:
        if not self._cached_item_temp_names:
            return item

        for cached_item_temp_name in self._cached_item_temp_names:
            if cached_item_temp_name in item:
                del item[cached_item_temp_name]

        return item
