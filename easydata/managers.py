from typing import List

from easydata import models
from easydata.data import DataBag
from easydata.loaders import ObjectLoader
from easydata.mixins import ConfigMixin
from easydata.parsers import Base as BaseParser
from easydata.utils import mix

__all__ = ("ModelManager",)


class ModelManager(ConfigMixin):
    def __init__(self, model):
        self._model = model

        self._models: list = []

        self._item_parsers: dict = {}

        self._item_temp_names: List[str] = []

        self._config_properties: dict = {}

        self._data_processors_loader = ObjectLoader()
        self._item_processors_loader = ObjectLoader()

        self._process_model_obj(model)

        self._init_config()

    @property
    def data_variants_name(self):
        return self.config["ED_DATA_VARIANTS_NAME"]

    @property
    def data_variants_key_name(self):
        return self.config["ED_DATA_VARIANTS_KEY_NAME"]

    @property
    def data_variant_name(self):
        return self.config["ED_DATA_VARIANT_NAME"]

    def item_keys(self):
        return list(self._item_parsers.keys())

    def items(self):
        return self._item_parsers

    def get_item_val(self, item_key: str):
        return self._item_parsers[item_key]

    def process_item_parser(self, item_key: str, data: DataBag):
        item_parser = self._item_parsers[item_key]

        if isinstance(item_parser, (str, float, int, list, dict)):
            return item_parser
        elif isinstance(item_parser, models.ItemModel):
            data = data.copy(item_parser.model_manager)

            return item_parser.parse(data)
        elif isinstance(item_parser, BaseParser):
            return item_parser.parse(data)

        return item_parser(data)

    def parse_data_to_items(
        self,
        data=None,
        **kwargs,
    ):

        if not isinstance(data, DataBag):
            if data:
                kwargs["data"] = data

            data = DataBag(self, **kwargs)

        data = self._apply_data_processors(data)

        if data.has(self.data_variants_name):
            for variant_data in self._parse_variants_data(data):
                item = variant_data.get_all()

                item = self._apply_items_processors(item)

                yield self._remove_temp_item_keys(item)
        else:
            item = data.get_all()

            item = self._apply_items_processors(item)

            yield self._remove_temp_item_keys(item)

    def _apply_data_processors(self, data: DataBag) -> DataBag:
        for model in self._models:
            data = model.preprocess_data(data)

        data = mix.apply_processors(
            value=data,
            processors=list(self._data_processors_loader.values()),
        )

        for model in self._models:
            data = model.process_data(data)

        return data

    def _apply_items_processors(self, item: dict) -> dict:
        for model in self._models:
            item = model.preprocess_item(item)

        item = mix.apply_processors(
            value=item,
            processors=list(self._item_processors_loader.values()),
        )

        for model in self._models:
            item = model.process_item(item)

        return item

    def _remove_temp_item_keys(self, item: dict) -> dict:
        if not self._item_temp_names:
            return item

        for item_temp_name in self._item_temp_names:
            if item_temp_name in item:
                del item[item_temp_name]

        return item

    def _process_model_obj(self, model):
        if model.block_models:
            for model_block in model.block_models:
                self._process_model_obj(model_block)

        self._load_item_parsers_from_model(model)

        self._load_config_properties_from_model(model)

        if model.data_processors:
            self._data_processors_loader.add_list(model.data_processors)

        if model.items_processors:
            self._item_processors_loader.add_list(model.items_processors)

        self._models.append(model)

    def _init_config(self):
        # Init config key and values from models
        self.init_config(self._config_properties)

        # Init parsers config
        for parser_instance in self._item_parsers.values():
            if isinstance(parser_instance, BaseParser):
                parser_instance.init_config(self.config)

    def _load_item_parsers_from_model(self, model):
        for item_name, parser_method in mix.iter_attr_data_from_obj(model, "item"):
            if item_name.startswith("temp_"):
                item_name = item_name.replace("temp_", "")

                if item_name not in self._item_temp_names:
                    self._item_temp_names.append(item_name)
            else:
                # If parser from parent model is not temp, then delete it from
                # _item_temp_names list if exists, because child had temp parser
                # with the same item name.
                if item_name in self._item_temp_names:
                    self._item_temp_names.remove(item_name)

            self._item_parsers[item_name] = parser_method

    def _load_config_properties_from_model(self, model):
        config_data = mix.iter_attr_data_from_obj(
            obj=model, attr_prefix="ED", preserve_prefix=True
        )

        for config_name, config_value in config_data:
            self._config_properties[config_name] = config_value

    def _parse_variants_data(self, data):
        variants_data = data[self.data_variants_name]

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
