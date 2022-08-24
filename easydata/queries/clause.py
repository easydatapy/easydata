from typing import Any, Optional

from easydata.queries.base import QuerySearchBase

__all__ = ("OrClause",)


class OrClause(QuerySearchBase):
    def __init__(self, *query_searches):
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

            if value is not None:
                return value

        return None
