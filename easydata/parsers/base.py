from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

from easydata.data import DataBag
from easydata.mixins import ConfigMixin
from easydata.queries.base import QuerySearch
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
        query: Optional[QuerySearch] = None,
        query_params: Optional[dict] = None,
        from_item: Optional[str] = None,
        default: Optional[Any] = None,
        default_from_item: Optional[str] = None,
        source: Optional[str] = None,
        process_raw_value: Optional[Callable] = None,
        process_value: Optional[Callable] = None,
    ):

        if query and from_item:
            raise AttributeError("query attr cannot be set together with from_item!")

        self._query = query
        self._query_params = query_params
        self._from_item = from_item
        self._default = default
        self._default_from_item = default_from_item
        self._source = source
        self._process_raw_value = process_raw_value
        self._process_value = process_value

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        if self._from_item and isinstance(data, DataBag):
            value = data.get(self._from_item)
        else:
            if with_parent_data:
                query_params = self._parse_query_params(parent_data)
            else:
                query_params = self._parse_query_params(data)

            if with_parent_data and not self._source:
                data = parent_data

            value = self._parse_data_to_value(data=data, query_params=query_params)

        if self._process_raw_value:
            value = self._process_raw_value(value, data)

        value = self._parse_value(value, data)

        if self._process_value:
            value = self._process_value(value, data)

        return self._process_default_value(value, data)

    def _parse_data_to_value(
        self,
        data: DataBag,
        query_params: Optional[dict] = None,
    ) -> Any:

        source = self._source or "main"

        if self._query:
            return self._parse_query(
                query=self._query, data=data, source=source, query_params=query_params
            )

        return self._parse_default_data_value(data, source)

    def _parse_query_params(self, data):

        if not self._query_params:
            return None

        parsed_query_params = {}

        for query_param_key, query_param_parser in self._query_params.items():
            parsed_value = query_param_parser.parse(data)

            parsed_query_params[query_param_key] = parsed_value

        return parsed_query_params

    def _parse_query(
        self,
        query: QuerySearch,
        data: Any,
        source: str,
        query_params: Optional[dict] = None,
    ):

        return parse.query_search(
            query=query,
            data=data,
            source=source,
            query_params=query_params,
        )

    def _process_default_value(self, value, data):
        if value is None and self._default_from_item is not None:
            value = data.get(self._default_from_item)

        if value is None and self._default is not None:
            return self._default

        return value  # no default value was specified

    @abstractmethod
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        return value

    def _parse_default_data_value(
        self,
        data: Any,
        source: Optional[str],
    ) -> Any:

        return parse.default_data_value(data, source)
