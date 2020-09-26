import re
from json import dumps
from typing import Any, Iterable, Optional

from pyquery import PyQuery

from easydata.data import DataBag
from easydata.queries.base import QuerySearch


class ReQuery(QuerySearch):
    def __init__(
        self,
        query: str,
        dotall: bool = True,
        ignore_case: bool = False,
        bytes_to_string_decode: str = "utf-8",
    ):

        if query and query == "::all":
            raise ValueError("Regex pattern is required beside ::all!")

        if query and query.endswith("::all"):
            query = query.split("::all")[0]

            self._all = True
        else:
            self._all = False

        super().__init__(query)

        self._dotall = dotall
        self._ignore_case = ignore_case
        self._bytes_to_string_decode = bytes_to_string_decode

    def _parse(
        self,
        data: Any,
        query: Optional[str],
    ):

        if self._all:
            return list(self._iter_parse(data, query=query))

        for result in self._iter_parse(data, query=query):
            return result

    def _iter_parse(self, data: Any, query: Optional[str]) -> Iterable[Any]:
        if not query:
            raise ValueError("Query cannot be empty")

        flags = 0

        if self._dotall:
            flags = re.DOTALL

        if self._ignore_case:
            flags = flags | re.IGNORECASE if flags else re.IGNORECASE

        results = re.finditer(query, data, flags)

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
            data = data.outer_html()

        if isinstance(data, (dict, list)):
            data = dumps(data)

        if isinstance(data, bytes):
            data = data.decode(self._bytes_to_string_decode)

        if not isinstance(data, str):
            raise TypeError(
                "Provided data must type of string, DataBag, PyQuery, dict, list "
                "or bytes",
            )

        return data
