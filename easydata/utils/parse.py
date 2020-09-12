from typing import Any, Optional

from easydata.data import DataBag
from easydata.queries.base import QuerySearch
from easydata.types import RequiredQuerySearch


def query_search(
    query: RequiredQuerySearch,
    data: Any,
    source: str = "data",
) -> Any:

    return _query_to_value(query, data, source)


def default_data_value(
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
