from abc import ABC, abstractmethod
from typing import Any, Callable, List, Optional

from easydata.data import DataBag
from easydata.mixins import ConfigMixin
from easydata.queries.base import QuerySearch
from easydata.types import OptionalQuerySearch, RequiredQuerySearch
from easydata.utils import parse

__all__ = ("Base", "BaseData")


class Base(ConfigMixin, ABC):
    @abstractmethod
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:
        pass


class BaseData(Base, ABC):
    def __init__(
        self,
        query: OptionalQuerySearch = None,
        from_item: Optional[str] = None,
        default: Optional[Any] = None,
        default_from_item: Optional[str] = None,
        source: Optional[str] = None,
        process_raw_value: Optional[Callable] = None,
        process_value: Optional[Callable] = None,
    ):

        if query and from_item:
            raise AttributeError("query attr cannot be set together with from_item!")

        self._query = self._query_to_list(query)
        self._from_item = from_item
        self._default = default
        self._default_from_item = default_from_item
        self._source = source if source else "data"
        self._process_raw_value = process_raw_value
        self._process_value = process_value

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> str:

        if self._from_item and isinstance(data, DataBag):
            value = data.get(self._from_item)
        else:
            if with_parent_data:
                data = parent_data

            value = self._parse_data_to_value(data)

        if self._process_raw_value:
            value = self._process_raw_value(value, data)

        value = self._parse_value(value, data)

        if self._process_value:
            value = self._process_value(value, data)

        if value is None and self._default_from_item is not None:
            value = data.get(self._default_from_item)

        if value is None and self._default is not None:
            return self._default

        return value

    def _parse_data_to_value(
        self,
        data: DataBag,
    ) -> Any:

        if self._query:
            return self._parse_query(
                query=self._query,
                data=data,
                source=self._source,
            )

        return self._parse_default_data_value(data)

    def _parse_query(
        self,
        query: RequiredQuerySearch,
        data: Any,
        source: str,
    ):

        return parse.query_search(
            query=query,
            data=data,
            source=source,
        )

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        return value

    def _parse_default_data_value(
        self,
        data: Any,
    ) -> Any:

        return parse.default_data_value(data, self._source)

    def _query_to_list(
        self,
        query: OptionalQuerySearch,
    ) -> Optional[List[QuerySearch]]:
        return [query] if isinstance(query, QuerySearch) else query
