from typing import Any, Iterable, Optional

from easytxt.text import normalize
from pyquery import PyQuery

from easydata.data import DataBag
from easydata.queries.base import QuerySearch
from easydata.utils import pseudo

__all__ = (
    "PyQuerySearch",
    "PyQueryStrictSearch",
)

_pseudo_with_values = [
    "attr",
    "has_class",
]

_attr_shortcut_mappings = {
    "val": "value",
    "src": "src",
    "href": "href",
    "name": "name",
    "class": "class",
    "content": "content",
}


class PyQuerySearch(QuerySearch):
    def __init__(
        self,
        query: str,
        remove_query: Optional[str] = None,
        **kwargs,
    ):

        super().__init__(query, **kwargs)

        self._remove_query = remove_query

        self._first: bool = True
        self._attr: Optional[str] = None
        self._has_class: Optional[str] = None
        self._text: bool = False
        self._ntext: bool = False
        self._html: bool = False
        self._outer_html: bool = False
        self._items: bool = False
        self._iter: bool = False

        if self._query and "::" in self._query:
            self._initialize_custom_pseudo_keys()

    def parse(
        self,
        pq: PyQuery,
        query: Optional[str],
    ) -> Any:

        if self._iter:
            return self._iter_parse(pq, query=query)
        if self._items:
            return list(self._iter_parse(pq, query=query))
        else:
            pq = self._parse_pq(pq, query=query, first=self._first)

            return self._extract_data_from_pq(pq)

    def _iter_parse(
        self,
        pq: PyQuery,
        query: Optional[str],
    ) -> Iterable[Any]:

        pq = self._parse_pq(pq, query=query, first=False)

        for spq in pq.items():
            yield self._extract_data_from_pq(spq)

    def process_data(
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
            return pq.text() or None
        elif self._ntext:
            return normalize(pq.text()) or None if pq else None
        elif self._html:
            return pq.html() or None
        elif self._outer_html:
            return pq.outer_html() or None
        elif self._has_class:
            # Returns bool
            return pq.has_class(self._has_class)
        elif self._attr:
            return pq.attr(self._attr) or None

        return pq

    def _parse_pq(
        self,
        pq: PyQuery,
        query: Optional[str],
        first: bool = True,
    ) -> PyQuery:

        if query:
            pq = pq(query)

        if pq and first:
            pq = pq.eq(0)

        if self._remove_query and pq:
            pq = pq.clone().remove(self._remove_query)

        return pq

    def _initialize_custom_pseudo_keys(self):
        self._query, pseudo_key = pseudo.get_key_from_query(self._query)

        pseudo_key = self._process_pseudo_key_extension(pseudo_key)

        self._process_pseudo_key(pseudo_key)

    def _process_pseudo_key_extension(self, pseudo_key: str) -> str:
        pseudo_key, extension = pseudo.get_extension_value(
            pseudo_key=pseudo_key,
            pseudo_keys_with_separator_value=["attr", "has_class"],
        )

        if not extension:
            return pseudo_key

        if extension == "iter":
            self._iter = True
        elif extension == "items":
            self._items = True
        elif extension == "all":
            self._first = False
        else:
            raise ValueError(
                "Pseudo key extension {} is not supported. Currently supported "
                "are -items, -iter and -all".format(extension)
            )

        return pseudo_key

    def _process_pseudo_key(self, pseudo_key: str) -> None:
        if pseudo_key.startswith("attr"):
            self._attr = pseudo.get_value(pseudo_key)
        elif pseudo_key.startswith("has_class"):
            self._has_class = pseudo.get_value(pseudo_key)
        elif pseudo_key in _attr_shortcut_mappings:
            self._attr = _attr_shortcut_mappings[pseudo_key]
        elif pseudo_key == "text":
            self._text = True
        elif pseudo_key == "ntext":
            self._ntext = True
        elif pseudo_key == "html":
            self._html = True
        elif pseudo_key == "ohtml":
            self._outer_html = True
        elif pseudo_key == "items":
            self._items = True
        elif pseudo_key == "iter":
            self._iter = True
        else:
            raise ValueError(
                "Pseudo key '{}' is not supported. Currently supported are: text,"
                "ntext,html,ohtml,items,iter,has_class(<value>),attr(<value>),"
                "{}".format(pseudo_key, ",".join(_attr_shortcut_mappings.keys()))
            )


class PyQueryStrictSearch(PyQuerySearch):
    strict = True
