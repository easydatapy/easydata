from types import FunctionType
from typing import Any, Optional

from easydata.data import DataBag
from easydata.queries.base import QuerySearch


def query_search(
    query: QuerySearch,
    data: Any,
    source: str = "main",
    query_params: Optional[dict] = None,
) -> Any:

    return query.get(
        data=data,
        source=source,
        query_params=query_params,
    )


def default_data_value(
    data: Any,
    source: Optional[str],
) -> Any:

    return data[source] if isinstance(data, DataBag) else data


def variants_data(data: DataBag, source: str):
    original_variants_data: dict = data[source]

    total_variants = len(original_variants_data)

    for variant_key, variant_multi_data in original_variants_data.items():
        data_copy = data.copy()

        variant_data = variant_multi_data[0]

        data_copy[source] = variant_data
        data_copy["{}_variants".format(source)] = variant_multi_data
        data_copy["{}_variants_len".format(source)] = total_variants
        data_copy["{}_key".format(source)] = variant_key

        yield data_copy


def value_from_parser(
    parser: Any,
    data: Any,
    parent_data: Any,
    with_parent_data: bool,
    config,
):

    if isinstance(parser, FunctionType):
        return parser(data)
    else:
        return parser.init_config(config).parse(
            data=data,
            parent_data=parent_data,
            with_parent_data=with_parent_data,
        )
