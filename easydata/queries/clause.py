from typing import Any, Optional

from easydata.queries.base import QuerySearchBase

__all__ = (
    "OrClause",
    "WithClause",
)


class OrClause(QuerySearchBase):
    def __init__(
        self,
        *query_searches,
        strict_none: bool = True,
    ):

        self._strict_none = strict_none

        self._query_searches = query_searches

    def get(
        self,
        data: Any,
        source: str = "main",
        parent_data: Optional[Any] = None,
    ) -> Any:

        for query_search in self._query_searches:
            value = query_search.get(
                data=data,
                source=source,
                parent_data=parent_data,
            )

            if self._strict_none and value is not None:
                return value
            elif not self._strict_none and value:
                return value

        return None


class WithClause(QuerySearchBase):
    def __init__(self, *query_searches):
        self._query_searches = query_searches

    def get(
        self,
        data: Any,
        source: str = "main",
        parent_data: Optional[Any] = None,
    ) -> Any:

        query_searches = list(self._query_searches)

        init_query_search = query_searches.pop(0)

        query = init_query_search.query

        value = init_query_search.get(
            data=data,
            source=source,
            parent_data=parent_data,
        )

        for query_search in query_searches:
            if not value:
                raise ValueError("Value cannot be empty for query: %s " % query)

            query = query_search.query

            value = query_search.get(value)

        return value
