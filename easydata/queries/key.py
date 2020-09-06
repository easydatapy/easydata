from json import loads
from typing import Any, Iterable, Optional

from easydata.data import DataBag
from easydata.queries.base import QuerySearch


class KeyQuery(QuerySearch):
    def __init__(
        self,
        query: str = None,
        keys: bool = False,
        values: bool = False,
    ):

        self._query = query
        self._keys = keys
        self._values = values

    def keys(self):
        self._keys = True

        return self

    def values(self):
        self._values = True

        return self

    def _parse(
        self,
        data: Any,
    ):

        data = data.get(self._query)

        return self._process_data_key_values(data)

    def _iter_parse(
        self,
        data: Any,
    ) -> Iterable[Any]:

        jdata = self._parse(data)

        if not jdata:
            return None

        for sjdata in jdata:
            yield sjdata

    def _process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:

        if isinstance(data, DataBag):
            if isinstance(data[source], (dict, list)):
                return data[source]

            data_dict_source = "{}_dict".format(source)

            data_dict = data.get(data_dict_source)

            if not data_dict:
                data_dict = loads(data[source])

                data[data_dict_source] = data_dict

            return data_dict
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
