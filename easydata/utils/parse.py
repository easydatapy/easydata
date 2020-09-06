from typing import Any, List, Optional

from easydata.data import DataBag
from easydata.queries.base import QuerySearch
from easydata.types import RequiredQuerySearch


def query_search(
    query: RequiredQuerySearch,
    data: Any,
    source: str = "data",
) -> Any:

    return _query_to_value(query, data, source)


def query_search_iter(
    query: RequiredQuerySearch,
    data: Any,
    source: str = "data",
) -> Optional[List[Any]]:

    query = [query] if isinstance(query, QuerySearch) else query

    last_query = query[-1]

    value = data

    if len(query) > 1:
        value = _query_to_value(query[:-1], value)

    values_iter = last_query.get_iter(value, source)

    return [v for v in values_iter] if values_iter else None


def default_value(
    data: Any,
    source: Optional[str],
) -> Any:

    return data[source] if isinstance(data, DataBag) else data


def _query_to_value(
    query: RequiredQuerySearch,
    data: Any,
    source: str = "data",
) -> Any:

    query = [query] if isinstance(query, QuerySearch) else query

    for query_obj in query:
        data = query_obj.get(data, source)

    return data
