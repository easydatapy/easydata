from typing import Any, Dict, List

from easydata.mixins import ConfigMixin

__all__ = ("DataBag",)


class DataBag(ConfigMixin):
    def __init__(self, model, **kwargs) -> None:

        self._model = model

        if model:
            self.init_config(model.config)

        self._cached_results: Dict[str, Any] = {}

        for arg_name, arg_value in kwargs.items():
            self.add(arg_name, arg_value)

    def add(self, arg_name: str, arg_value):
        setattr(self, arg_name, arg_value)

    def get(self, item_name: str) -> Any:
        """Each item class field or item method are called only once
        and results are cached which leads to a faster performance!"""

        if item_name in self._cached_results:
            return self._cached_results[item_name]

        self._cached_results[item_name] = self._model.parse_item_properties(
            item_name, self
        )

        return self._cached_results[item_name]

    def get_multi(self, item_names: List[str]) -> dict:
        results = {}

        for item_name in item_names:
            results[item_name] = self.get(item_name)

        return results

    def copy(self):
        data_copy = self.__dict__.copy()

        del data_copy["_model"]
        del data_copy["_cached_results"]

        return DataBag(model=self._model, **data_copy)

    @property
    def cached_results(self):
        return self._cached_results

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)
