from typing import Any, Iterable, Optional

from easytxt.text import normalize
from pyquery import PyQuery

from easydata.data import DataBag
from easydata.queries.base import QuerySearch


class PyQuerySearch(QuerySearch):
    def __init__(
        self,
        query: Optional[str] = None,
        attr: Optional[str] = None,
        rm: Optional[str] = None,
        text: bool = False,
        ntext: bool = False,
        html: bool = False,
        first: bool = True,
        items: bool = False,
    ):

        self._query = query
        self._attr = attr
        self._rm_query = rm
        self._text = text
        self._ntext = ntext
        self._html = html
        self._first = first
        self._items = items

    def attr(self, attr: str):
        self._attr = attr

        return self

    @property
    def val(self):
        return self.attr("value")

    @property
    def src(self):
        return self.attr("src")

    @property
    def href(self):
        return self.attr("href")

    @property
    def text(self):
        self._text = True

        return self

    @property
    def ntext(self):
        self._ntext = True

        return self

    @property
    def html(self):
        self._html = True

        return self

    @property
    def items(self):
        self._items = True

        return self

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
