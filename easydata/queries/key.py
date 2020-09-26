import json
from typing import Any, Optional, Tuple

import yaml

from easydata.data import DataBag
from easydata.queries.base import QuerySearch
from easydata.utils import pseudo


class KeyQuery(QuerySearch):
    def __init__(
        self,
        query: str = None,
    ):

        super().__init__(query)

        self._keys: bool = False
        self._values: bool = False
        self._json: bool = False
        self._yaml: bool = False
        self._str: bool = False
        self._dict_key_value: Optional[Tuple[str, str]] = None

        if self._query and "::" in self._query:
            self._initialize_custom_pseudo_keys()

    def _parse(
        self,
        data: Any,
        query: Optional[str],
    ):

        if query:
            data = data.get(query)

        return self._process_data_key_values(data)

    def _process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:

        if isinstance(data, DataBag):
            if isinstance(data[source], (dict, list)):
                return data[source]

            # If data is json, then it will be attempted to be converted to dict or
            # list. Conversion will be stored in a DataBag object under different
            # source name, so that we don't load json data each time.
            data_dict_source = "{}_dict".format(source)

            if hasattr(data, data_dict_source):
                return data[data_dict_source]

            try:
                data_dict = json.loads(data[source])

                data[data_dict_source] = data_dict

                return data_dict
            except Exception:
                raise ValueError(
                    "Provided data from source {} could not be converted to dict or "
                    "list in order to use query!".format(source)
                )
        elif isinstance(data, (dict, list)):
            return data

        return json.loads(data)

    def _process_data_key_values(self, data):
        if data:
            if self._dict_key_value:
                if not isinstance(data, list):
                    raise TypeError(
                        "Pseudo key dict(<key>:<value>) will make list to dict "
                        "conversion if queried data is list type."
                    )

                dict_key, dict_value = self._dict_key_value

                data = {ddata[dict_key]: ddata[dict_value] for ddata in data}

            if self._values:
                data = list(data.values())

            if self._keys:
                data = list(data.keys())

            if self._json:
                data = json.dumps(data)

            if self._yaml:
                data = yaml.dump(data)

            if self._str and not isinstance(data, str):
                data = str(data)

        return data

    def _initialize_custom_pseudo_keys(self):
        self._query, pseudo_key = pseudo.get_key_from_query(self._query)

        pseudo_key = self._process_pseudo_key_extension(pseudo_key)

        self._process_pseudo_key(pseudo_key)

    def _process_pseudo_key_extension(self, pseudo_key: str) -> str:
        pseudo_key, extension = pseudo.get_extension_value(pseudo_key, ["dict"])

        if not extension:
            return pseudo_key

        if extension == "json":
            self._json = True
        elif extension == "yaml":
            self._yaml = True
        elif extension == "str":
            self._str = True
        else:
            raise ValueError(
                "Pseudo key extension {} is not supported. Currently supported "
                "is only -json".format(extension)
            )

        return pseudo_key

    def _process_pseudo_key(self, pseudo_key: str) -> None:
        if pseudo_key.startswith("dict"):
            dict_key_value_text = pseudo_key.split("(")[-1].split(")")[0]

            dict_key_value_split = dict_key_value_text.split(":")

            self._dict_key_value = dict_key_value_split[0], dict_key_value_split[1]
        elif pseudo_key == "values":
            self._values = True
        elif pseudo_key == "keys":
            self._keys = True
        elif pseudo_key == "json":
            self._json = True
        elif pseudo_key == "yaml":
            self._yaml = True
        elif pseudo_key == "str":
            self._str = True
        else:
            raise ValueError(
                "Pseudo key '{}' is not supported. Currently supported are: keys,"
                "values, dict(<key>,<value>).".format(pseudo_key)
            )
