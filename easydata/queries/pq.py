from typing import Any, Iterable, Optional

from easytxt.text import normalize
from pyquery import PyQuery

from easydata.data import DataBag
from easydata.queries.base import QuerySearch

_attr_shortcut_mappings = {
    "val": "value",
    "src": "src",
    "href": "href",
    "name": "name",
    "content": "content",
}


class PyQuerySearch(QuerySearch):
    def __init__(
        self,
        query: Optional[str] = None,
        remove_query: Optional[str] = None,
    ):

        self._query = query
        self._remove_query = remove_query

        self._first: bool = True
        self._attr: Optional[str] = None
        self._text: bool = False
        self._ntext: bool = False
        self._html: bool = False
        self._items: bool = False

        if self._query and "::" in self._query:
            self._initialize_custom_pseudo_keys()

    def _parse(
        self,
        pq: PyQuery,
    ) -> Any:

        if self._items:
            return [i for i in self._iter_parse(pq)]
        else:
            pq = self._parse_pq(pq, self._first)

            return self._extract_data_from_pq(pq)

    def _iter_parse(
        self,
        pq: PyQuery,
    ) -> Iterable[Any]:

        pq = self._parse_pq(pq, first=False)

        for spq in pq.items():
            yield self._extract_data_from_pq(spq)

    def _process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Optional[PyQuery]:

        if isinstance(data, DataBag):
            if isinstance(data[source], PyQuery):
                return data[source]

            pq_source = "{}_pq".format(source)

            if not hasattr(data, pq_source):
                data[pq_source] = PyQuery(data[source])

            return data[pq_source]
        elif isinstance(data, PyQuery):
            return data

        return PyQuery(data)

    def _extract_data_from_pq(self, pq: PyQuery) -> Any:
        if self._text:
            return pq.text()
        elif self._ntext:
            return normalize(pq.text()) if pq else None
        elif self._html:
            return pq.html()
        elif self._attr:
            return pq.attr(self._attr)

        return pq

    def _parse_pq(
        self,
        pq: PyQuery,
        first: bool = True,
    ) -> PyQuery:

        if self._query:
            pq = pq(self._query)

        if pq and first:
            pq = pq.eq(0)

        if self._remove_query and pq:
            pq = pq.clone().remove(self._remove_query)

        return pq

    def _initialize_custom_pseudo_keys(self):
        query_parts = self._query.split("::")

        self._query = None if self._query.startswith("::") else query_parts[0]

        pseudo_key = query_parts[-1]

        pseudo_key = self._process_pseudo_key_extension(pseudo_key)

        self._process_pseudo_key(pseudo_key)

    def _process_pseudo_key_extension(self, pseudo_key: str) -> str:
        # Attributes can have attribute value with - in it, so we must sure that it
        # has extension. Otherwise we just ignore it.
        if pseudo_key.startswith("attr") and ")-" not in pseudo_key:
            return pseudo_key
        elif "-" not in pseudo_key:
            return pseudo_key  # doesn't have extension

        pseudo_key_parts = pseudo_key.split("-")

        # If split by - produces more than 2 list items that means that we are dealing
        # with attr value that has - in it.
        if len(pseudo_key_parts) > 2:
            pseudo_key = "-".join(pseudo_key_parts[:-1])
        else:
            pseudo_key = pseudo_key_parts[0]

        pseudo_key_extension = pseudo_key_parts[-1]

        if pseudo_key_extension == "items":
            self._items = True
        elif pseudo_key_extension == "all":
            self._first = False
        else:
            raise ValueError(
                "Pseudo key extension {} is not supported. Currently supported "
                "are -items and -all".format(pseudo_key_extension)
            )

        return pseudo_key

    def _process_pseudo_key(self, pseudo_key: str) -> None:
        if pseudo_key.startswith("attr"):
            attr_value = pseudo_key.split("(")[-1].strip(")")
            self._attr = attr_value
        elif pseudo_key in _attr_shortcut_mappings:
            self._attr = _attr_shortcut_mappings[pseudo_key]
        elif pseudo_key == "text":
            self._text = True
        elif pseudo_key == "ntext":
            self._ntext = True
        elif pseudo_key == "html":
            self._html = True
        elif pseudo_key == "items":
            self._items = True
        else:
            raise ValueError(
                "Pseudo key '{}' is not supported. Currently supported are: text,"
                "ntext,html,items, attr(<value>),{}".format(
                    pseudo_key, ",".join(_attr_shortcut_mappings.keys())
                )
            )
