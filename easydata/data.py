from typing import Any, Dict, List

from easydata.mixins import ConfigMixin

__all__ = ("DataBag",)


class DataBag(ConfigMixin):
    def __init__(
        self,
        model_manager=None,
        **kwargs,
    ) -> None:

        self._model_manager = model_manager

        if model_manager:
            self.init_config(model_manager.config)

        self._cached_results: Dict[str, Any] = {}

        for arg_name, arg_value in kwargs.items():
            self.add(arg_name, arg_value)

    def add(self, arg_name: str, arg_value):
        setattr(self, arg_name, arg_value)

    def has(self, arg_name):
        return hasattr(self, arg_name)

    def get(self, item_key: str) -> Any:
        """Each item class field or item method are called only once
        and results are cached which leads to a faster performance!"""

        if item_key in self._cached_results:
            return self._cached_results[item_key]

        self._cached_results[item_key] = self._model_manager.process_item_parser(
            item_key=item_key,
            data=self,
        )

        return self._cached_results[item_key]

    def get_all(self) -> dict:
        return self.get_multi(self._model_manager.item_keys())

    def get_multi(self, item_keys: List[str]):
        results = {}

        for item_key in item_keys:
            results[item_key] = self.get(item_key)

        return results

    def copy(self, model_manager=None):
        data_copy = self.__dict__.copy()

        del data_copy["_model_manager"]
        del data_copy["_cached_results"]

        if model_manager:
            return DataBag(
                model_manager=model_manager,
                **data_copy,
            )

        return DataBag(
            model_manager=self._model_manager,
            **data_copy,
        )

    @property
    def cached_results(self):
        return self._cached_results

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)
