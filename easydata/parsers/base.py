from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Union

from easydata.data import DataBag
from easydata.mixins import ConfigMixin
from easydata.queries.base import QuerySearchBase
from easydata.utils import parse

__all__ = (
    "Base",
    "BaseData",
)


class Base(ConfigMixin, ABC):
    @abstractmethod
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:
        pass


def custom_process_value(
    callback_or_parser: Union[Callable, Base],
    value: Any,
    data: Any,
):

    if isinstance(callback_or_parser, Base):
        return callback_or_parser.parse(value)

    return callback_or_parser(value, data)


class BaseData(Base, ABC):
    def __init__(
        self,
        query: Optional[Union[QuerySearchBase, BaseData]] = None,
        from_item: Optional[str] = None,
        default: Optional[Any] = None,
        default_from_item: Optional[str] = None,
        source: Optional[str] = None,
        process_raw_value: Optional[Union[Callable, Base]] = None,
        process_value: Optional[Union[Callable, Base]] = None,
        debug: bool = False,
        debug_source: bool = None,
    ):

        if query and from_item:
            raise AttributeError("query attr cannot be set together with from_item!")

        self._query = query
        self._from_item = from_item
        self._default = default
        self._default_from_item = default_from_item
        self._source = source
        self._process_raw_value = process_raw_value
        self._process_value = process_value
        self._debug = debug
        self._debug_source = debug_source

    def add_query(self, query: Union[QuerySearchBase, BaseData]):
        self._query = query

    def add_source(self, source: str):
        self._source = source

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        if self._from_item and isinstance(data, DataBag):
            value = data.get(self._from_item)
        else:
            parent_data = parent_data if with_parent_data else data

            if with_parent_data and not self._source:
                data = parent_data

            value = self._parse_data_to_value(
                data=data,
                parent_data=parent_data,
            )

        if self._debug_source:  # Debug value before is parsed
            print(value)

        if self._process_raw_value:
            value = custom_process_value(self._process_raw_value, value, data)

        value = self.parse_value(value, data)

        if self._debug:  # Debug value after is parsed
            print(value)

        if self._process_value:
            value = custom_process_value(self._process_value, value, data)

        return self._process_default_value(value, data)

    @property
    def source(self):
        return self._source or "main"

    def _parse_data_to_value(
        self,
        data: DataBag,
        parent_data: Optional[DataBag] = None,
    ) -> Any:

        if self._query:
            return self._parse_query(
                query=self._query,
                data=data,
                source=self.source,
                parent_data=parent_data,
            )

        return self._parse_default_data_value(data, self.source)

    def _parse_query(
        self,
        query: Union[QuerySearchBase, BaseData],
        data: Any,
        source: str,
        parent_data: Optional[Any] = None,
    ):

        return parse.query_parser(
            query=query,
            data=data,
            source=source,
            parent_data=parent_data,
        )

    def _process_default_value(self, value, data):
        if value is None and self._default_from_item is not None:
            value = data.get(self._default_from_item)

        if value is None and self._default is not None:
            return self._default

        return value  # no default value was specified

    @abstractmethod
    def parse_value(
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
