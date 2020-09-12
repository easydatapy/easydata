from json import loads
from typing import Any, Optional

from easydata.data import DataBag
from easydata.queries.base import QuerySearch


class KeyQuery(QuerySearch):
    def __init__(
        self,
        query: str = None,
    ):

        self._query = query
        self._keys = False
        self._values = False

        if self._query and "::" in self._query:
            self._initialize_custom_pseudo_keys()

    def _parse(
        self,
        data: Any,
    ):

        if self._query:
            data = data.get(self._query)

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
                data_dict = loads(data[source])

                data[data_dict_source] = data_dict

                return data_dict
            except Exception:
                raise ValueError(
                    "Provided data from source {} could not be converted to dict or "
                    "list in order to use key query!".format(source)
                )
        elif isinstance(data, (dict, list)):
            return data

        return loads(data)

    def _process_data_key_values(self, data):
        if data:
            if self._values:
                data = list(data.values())

            if self._keys:
                data = list(data.keys())

        return data

    def _initialize_custom_pseudo_keys(self):
        query_parts = self._query.split("::")

        self._query = None if self._query.startswith("::") else query_parts[0]

        pseudo_key = query_parts[-1]

        if pseudo_key == "values":
            self._values = True
        elif pseudo_key == "keys":
            self._keys = True
        else:
            raise ValueError(
                "Pseudo key '{}' is not supported. Currently supported are: keys,"
                "values".format(pseudo_key)
            )
