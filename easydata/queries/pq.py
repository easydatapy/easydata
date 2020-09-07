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
        rm: Optional[str] = None,
        first: bool = True,
    ):

        self._query = query
        self._rm_query = rm
        self._first = first

        self._attr = None
        self._text = False
        self._ntext = False
        self._html = False
        self._items = False

        if self._query and "::" in self._query:
            self._initialize_custom_pseudo_keys()

    def rm(self, query: str):
        self._rm_query = query

        return self

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

        if self._rm_query and pq:
            pq = pq.clone().remove(self._rm_query)

        return pq

    def _initialize_custom_pseudo_keys(self):
        query_parts = self._query.split("::")

        self._query = None if self._query.startswith("::") else query_parts[0]

        pseudo_key = query_parts[-1]

        if "-items" in pseudo_key:
            pseudo_key = pseudo_key.split("-")[0]

            self._items = True

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
                "Pseudo type '{}' is not supported for extraction type. Currently "
                "supported are: text,ntext,html,items,<pseudo el>-items, "
                "attr(<value>),{}".format(
                    pseudo_key, ",".join(_attr_shortcut_mappings.keys())
                )
            )
