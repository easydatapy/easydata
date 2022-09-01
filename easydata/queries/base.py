from abc import ABC, abstractmethod
from typing import Any, Optional

from easydata.exceptions import QuerySearchDataEmpty, QuerySearchResultNotFound
from easydata.utils import validate

__all__ = (
    "QuerySearchBase",
    "QuerySearch",
)


class QuerySearchBase(ABC):
    @abstractmethod
    def get(
        self,
        data: Any,
        source: str = "main",
        parent_data: Optional[Any] = None,
    ) -> Any:
        pass


class QuerySearch(QuerySearchBase, ABC):
    strict: bool = False

    def __init__(
        self,
        query: str,
        params: Optional[dict] = None,
        source: Optional[str] = None,
        strict: Optional[bool] = None,
        empty_as_none: bool = False,
        debug_query: bool = False,
    ):

        self._query = query
        self._source = source
        self._params = params
        self._empty_as_none = empty_as_none
        self._debug_query = debug_query

        if isinstance(strict, bool):
            self.strict = strict

    def add_query_prefix(self, query_prefix: str):
        self._query = query_prefix + self._query

    @property
    def query(self):
        return self._query

    def get(
        self,
        data: Any,
        source: str = "main",
        parent_data: Optional[Any] = None,
    ) -> Any:

        source = self._source or source

        validate.if_data_bag_with_source(
            data=data,
            source=source,
        )

        query_params = self._parse_query_params(parent_data or data)

        if not data:
            if self.strict and data is None:
                error_msg = 'Query: "%s" cannot be performed because data is empty!'

                raise QuerySearchDataEmpty(error_msg, self._query)

            return None

        data = self.process_data(data, source)

        if self._query and query_params:
            query = self._apply_query_params(self._query, query_params)
        else:
            query = self._query

        if self._debug_query:
            print(query)

        value = self.parse(data, query)

        if not value and self._empty_as_none:
            value = None

        if self.strict and value is None:
            error_msg = 'Query: "%s" didn\'t found any results!'

            raise QuerySearchResultNotFound(error_msg, self._query)

        return value

    def _parse_query_params(self, data: Any):

        if not self._params:
            return None

        parsed_query_params = {}

        for query_param_key, query_param_parser in self._params.items():
            parsed_value = query_param_parser.parse(data)

            parsed_query_params[query_param_key] = parsed_value

        return parsed_query_params

    def _apply_query_params(self, query, query_params):
        return query.format(**query_params)

    @abstractmethod
    def parse(
        self,
        data: Any,
        query: Optional[str],
    ):
        pass

    @abstractmethod
    def process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:
        pass
