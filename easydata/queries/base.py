from abc import ABC, abstractmethod
from typing import Any, Optional

from easydata.exceptions import QuerySearchDataEmpty, QuerySearchResultNotFound
from easydata.utils import validate


class QuerySearchBase(ABC):
    @abstractmethod
    def get(
            self,
            data: Any,
            source: str = "main",
            query_params: Optional[dict] = None,
    ) -> Any:
        pass


class QuerySearch(QuerySearchBase, ABC):
    strict: bool = False

    def __init__(
        self,
        query: str = None,
        source: Optional[str] = None,
        strict: Optional[bool] = None,
    ):

        self._query = query
        self._source = source

        if isinstance(strict, bool):
            self.strict = strict

    def get(
        self,
        data: Any,
        source: str = "main",
        query_params: Optional[dict] = None,
    ) -> Any:

        validate.if_data_bag_with_source(
            data=data,
            source=self._source or source,
        )

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

        value = self.parse(data, query)

        if self.strict and value is None:
            error_msg = 'Query: "%s" didn\'t found any results!'

            raise QuerySearchResultNotFound(error_msg, self._query)

        return value

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
