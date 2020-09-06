import re
from json import dumps
from typing import Any, Iterable, Optional, Union

from pyquery import PyQuery

from easydata.data import DataBag
from easydata.queries.base import QuerySearch


class ReQuery(QuerySearch):
    def __init__(
        self,
        query: Union[str, bytes],
        flag: int = re.DOTALL,
        bytes_to_string_decode: str = "utf-8",
    ):

        self._query = re.compile(query, flag)
        self._bytes_to_string_decode = bytes_to_string_decode

    def _parse(
        self,
        data: Any,
    ):

        for result in self._iter_parse(data):
            return result

    def _iter_parse(
        self,
        data: Any,
    ) -> Iterable[Any]:

        results = re.finditer(self._query, data)

        for result in results:
            yield result.group(1)

    def _process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:

        if isinstance(data, DataBag):
            data = data[source]

        if isinstance(data, PyQuery):
            data = data.html()

        if isinstance(data, (dict, list)):
            data = dumps(data)

        if isinstance(data, bytes):
            data = data.decode(self._bytes_to_string_decode)

        if not isinstance(data, str):
            raise TypeError("Provided data must be string in order to make re search")

        return data
