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

        self.query = re.compile(query, flag)
        self.bytes_to_string_decode = bytes_to_string_decode

    def parse(
        self,
        data: Any,
    ):

        for result in self.iter_parse(data):
            return result

    def iter_parse(
        self,
        data: Any,
    ) -> Iterable[Any]:

        results = re.finditer(self.query, data)

        for result in results:
            yield result.group(1)

    def process_data(
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
            data = data.decode(self.bytes_to_string_decode)

        if not isinstance(data, str):
            raise TypeError("Provided data must be string in order to make re search")

        return data
