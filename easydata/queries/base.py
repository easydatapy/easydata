from abc import ABC, abstractmethod
from typing import Any, Optional

from easydata.utils import validate


class QuerySearch(ABC):
    def __init__(
        self,
        query: str = None,
    ):

        self._query = query

    def get(
        self,
        data: Any,
        source: str = "main",
        query_params: Optional[dict] = None,
    ) -> Any:

        validate.if_data_bag_with_source(
            data=data,
            source=source,
        )

        if not data:
            return None

        data = self._process_data(data, source)

        if self._query and query_params:
            query = self._apply_query_params(self._query, query_params)
        else:
            query = self._query

        return self._parse(data, query)

    def _apply_query_params(self, query, query_params):
        return query.format(**query_params)

    @abstractmethod
    def _parse(
        self,
        data: Any,
        query: Optional[str],
    ):
        pass

    @abstractmethod
    def _process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:
        pass
