from types import GeneratorType
from typing import Any, Iterator, List

from easydata import models
from easydata.data import DataBag
from easydata.loaders import ObjectLoader
from easydata.mixins import ConfigMixin
from easydata.parsers import Base as BaseParser
from easydata.utils import mix

__all__ = ("ModelManager",)

MODEL_VARIANTS_KEYS = [
    "variants_query",
    "variants_source",
    "variants_key_parser",
    "variants_key_query",
]


class ModelManager(ConfigMixin):
    _ignore_item_attr_prefix = ["item_processors"]

    def __init__(self, model):
        self._model = model

        self._models: list = []

        self._data_iter_query_processor = None

        self._data_variants_processor = None

        self._item_parsers: dict = {}

        self._item_protected_names: List[str] = []

        self._config_properties: dict = {}

        self._data_processors_loader = ObjectLoader()

        self._item_processors_loader = ObjectLoader()

        self._init_model(model)

        self._init_config()

        self._init_parsers_config()

    @property
    def data_processors(self) -> ObjectLoader:
        return self._data_processors_loader

    @property
    def item_processors(self) -> ObjectLoader:
        return self._item_processors_loader

    def item_keys(self):
        return list(self._item_parsers.keys())

    def items(self):
        return self._item_parsers

    def get_item_val(self, item_key: str):
        return self._item_parsers[item_key]

    def process_item_parser(self, item_key: str, data: DataBag):
        item_parser = self._item_parsers[item_key]

        if not item_parser:
            return None

        if isinstance(item_parser, (str, float, int, list, dict)):
            return item_parser
        elif isinstance(item_parser, models.ItemModel):
            data = data.copy(item_parser.model_manager)

            return item_parser.parse_item(data)
        elif isinstance(item_parser, BaseParser):
            return item_parser.parse(data)

        return item_parser(data)

    def parse_data_to_items(
        self,
        data=None,
        **kwargs,
    ) -> Iterator[dict]:

        if not isinstance(data, DataBag):
            if data:
                kwargs["main"] = data

            data = DataBag(**kwargs)

        if not data.has_model_manger_instance():
            data.init_model_manager(self)

        drop_item_exceptions = []

        for iter_data in self._apply_data_processors(data):
            try:
                yield self._data_to_item(iter_data)
            except self._drop_item_exception as drop_item_exception:
                # we store drop item exceptions so that other variations could
                # get processed and we throw stored exceptions after iteration
                # has ended
                drop_item_exceptions.append(drop_item_exception)

        if drop_item_exceptions:
            if len(drop_item_exceptions) > 1:
                raise self._drop_item_exception(drop_item_exceptions)

            raise drop_item_exceptions[0]

    @property
    def _drop_item_exception(self):
        return self.config["ED_DROP_ITEM_EXCEPTION"]

    def _apply_data_processors(self, data: DataBag) -> Iterator[DataBag]:
        data = self._process_models_preprocess_data(data)

        data_processors = list(self._data_processors_loader.values())

        if data_processors:
            for iter_data in self._apply_processors(data, data_processors):
                iter_data = self._process_models_process_data(iter_data)

                yield iter_data
        else:
            yield data

    def _process_models_process_data(self, data: DataBag):
        for model in self._models:
            data = model.process_data(data)

        return data

    def _apply_processors(
        self,
        value: Any,
        processors: list,
    ) -> Any:

        for processor in processors:
            value = self._apply_processor(processor, value)

        yield from value

    def _apply_processor(self, processor, value):
        if isinstance(value, GeneratorType):
            for iter_value in value:
                yield from processor.parse(iter_value)
        else:
            yield from processor.parse(value)

    def _process_models_preprocess_data(self, data: DataBag):
        for model in self._models:
            data = model.preprocess_data(data)

        return data

    def _apply_item_processors(self, item: dict) -> dict:
        for model in self._models:
            item = model.preprocess_item(item)

        item = mix.apply_processors(
            value=item,
            processors=list(self._item_processors_loader.values()),
        )

        for model in self._models:
            item = model.process_item(item)

        return item

    def _remove_protected_item_keys(self, item: dict) -> dict:
        if not self._item_protected_names:
            return item

        for item_protected_name in self._item_protected_names:
            if item_protected_name in item:
                del item[item_protected_name]

        return item

    def _data_to_item(self, data: DataBag):
        item = data.get_all()

        item = self._apply_item_processors(item)

        return self._remove_protected_item_keys(item)

    def _init_model(self, model):
        if hasattr(model, "block_models"):
            for model_block in getattr(model, "block_models"):
                self._init_model(model_block)

        model.init_model()

        self._load_item_parsers_from_model(model)

        self._load_config_properties_from_model(model)

        if hasattr(model, "data_processors"):
            data_processors = getattr(model, "data_processors")

            self._data_processors_loader.add_list(data_processors)

        if hasattr(model, "item_processors"):
            item_processors = getattr(model, "item_processors")

            self._item_processors_loader.add_list(item_processors)

        model.initialized_model()

        self._models.append(model)

    def _init_config(self):
        self.init_config(self._config_properties)

    def _init_parsers_config(self):
        for parser_instance in self._item_parsers.values():
            if isinstance(parser_instance, BaseParser):
                parser_instance.init_config(self.config)

    def _load_item_parsers_from_model(self, model):
        item_attr_items = mix.iter_attr_data_from_obj(
            obj=model,
            attr_prefixes=["item_", "_item_"],
            ignore_attr_prefix=self._ignore_item_attr_prefix,
        )

        for item_name, parser_method in item_attr_items:
            if item_name.startswith("item_"):
                item_name = item_name.replace("item_", "")

            if item_name.startswith("_item_"):
                item_name = item_name.replace("_item_", "")

                if item_name not in self._item_protected_names:
                    self._item_protected_names.append(item_name)
            else:
                # If item parser from parent model is not protected, then
                # delete it from _item_protected_names list if exists, because
                # child had protected item parser with the same item name.
                if item_name in self._item_protected_names:
                    self._item_protected_names.remove(item_name)

            self._item_parsers[item_name] = parser_method

    def _load_config_properties_from_model(self, model):
        config_data = mix.iter_attr_data_from_obj(
            obj=model,
            attr_prefixes=["ED_"],
        )

        for config_name, config_value in config_data:
            self._config_properties[config_name] = config_value
