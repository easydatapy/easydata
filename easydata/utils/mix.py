from types import GeneratorType
from typing import Any, Callable, List, Optional, Union

from easytxt.text import to_list as multiply_to_list
from pyquery import PyQuery

from easydata import groups
from easydata.config.loader import ConfigLoader
from easydata.data import DataBag
from easydata.parsers.base import Base
from easydata.processors.base import BaseProcessor


def _parse_float(
    value: Any,
) -> Optional[float]:

    if isinstance(value, float):
        return value

    if isinstance(value, int):
        return float(value)

    return float(value) if is_str_float(value) else None


def _parse_int(value: str):
    try:
        return int(value)
    except ValueError:
        return None


def unique_list(list_data: list) -> list:
    unique_list_data = []

    for data in list_data:
        if data not in unique_list_data:
            unique_list_data.append(data)

    return unique_list_data


def tuple_list_to_dict(
    tuple_list: List[Union[tuple, str]],
    default: Optional[str] = None,
) -> dict:

    dict_data = {}

    for list_data in tuple_list:
        if isinstance(list_data, tuple):
            key, value = list_data

            dict_data[key] = value
        else:
            dict_data[list_data] = default

    return dict_data


def pq_remove_nodes(
    pq: PyQuery,
    css_remove: Union[str, list],
) -> PyQuery:

    pq = pq.clone()

    if isinstance(css_remove, str):
        css_remove = [css_remove]

    for remove_node in css_remove:
        pq.remove(remove_node)

    return pq


def pq_extract_value_items(
    pq: PyQuery,
    css: Optional[str] = None,
    css_remove: Optional[Union[str, list]] = None,
):

    if css:
        pq = pq(css)

    if css_remove:
        pq = pq_remove_nodes(pq, css_remove)

    return pq.items()


def init_processors_config(
    processors: list,
    config: ConfigLoader,
):

    for processor in processors:
        if isinstance(processor, BaseProcessor):
            processor.init_config(config)


def apply_processors(
    value: Any,
    processors: list,
    return_on_none: bool = False,
) -> Any:

    for processor in processors:
        if isinstance(processor, BaseProcessor):
            value = processor.parse(value)
        else:
            value = processor(value)

        if not value and return_on_none:
            return None

    return value


def extract_attr_names_from_obj(
    obj: object,
    attr_prefixes: List[str],
    ignore_attr_prefix: Optional[List[str]] = None,
):

    attr_names = []

    for attr_name in dir(obj):
        if ignore_attr_prefix:
            if any(attr_name.startswith(sk) for sk in ignore_attr_prefix):
                continue

        if any(attr_name.startswith(ap) for ap in attr_prefixes):
            attr_names.append(attr_name)

    return attr_names


def iter_attr_data_from_obj(
    obj: object,
    attr_prefixes: List[str],
    ignore_attr_prefix: Optional[List[str]] = None,
):

    attr_names = extract_attr_names_from_obj(
        obj=obj,
        attr_prefixes=attr_prefixes,
        ignore_attr_prefix=ignore_attr_prefix,
    )

    for attr_name in attr_names:
        attr_value = getattr(obj, attr_name)

        if isinstance(attr_value, type(groups.ItemGroup)):
            attr_value = attr_value()

        yield attr_name, attr_value


def data_to_data_bag(
    data: Optional[Union[Any, DataBag]] = None,
    **kwargs,
):

    if not isinstance(data, DataBag):
        if data:
            kwargs["main"] = data

        return DataBag(**kwargs)

    if kwargs:
        for data_name, data_value in kwargs.items():
            data.add(data_name, data_value)

    return data


def apply_data_processor(processor, value):
    if isinstance(value, GeneratorType):
        for iter_value in value:
            yield from processor.parse(iter_value)
    else:
        yield from processor.parse(value)


def apply_data_processors(
    value: Any,
    processors: list,
) -> Any:

    for processor in processors:
        value = apply_data_processor(processor, value)

    yield from value


def to_list(
    value: Any,
    split_key: Union[List[str], str],
) -> list:

    if not value:
        return []

    if isinstance(split_key, str):
        split_key = [split_key]

    value = str(value)

    for single_split_key in split_key:
        if single_split_key in value:
            return [v.strip() for v in value.split(single_split_key)]

    return [value]


def multiply_list_values(
    list_values: list,
    multiply_keys: Optional[Union[list, tuple]] = None,
) -> list:

    new_all_list_values = []

    for list_value in list_values:
        if not list_value:
            continue

        new_list_values = multiply_to_list(
            value=list_value,
            multiply_keys=multiply_keys,
        )

        for new_list_value in new_list_values:
            if new_list_value:
                new_all_list_values.append(new_list_value)

    return new_all_list_values


def multiply_list_values_by_split_key(
    list_values: list,
    split_key: Union[List[str], str],
) -> list:

    new_all_list_values = []

    for list_value in list_values:
        if not list_value:
            continue

        new_list_values = to_list(
            value=list_value,
            split_key=split_key,
        )

        for new_list_value in new_list_values:
            if new_list_value:
                new_all_list_values.append(new_list_value)

    return new_all_list_values


def filter_list_by_bool_callable(
    list_values: List[Any],
    data: Any,
    callable_param: Callable,
):

    filtered_list_values = []

    for value in list_values:
        ignore: bool = callable_param(value, data)

        if not isinstance(ignore, bool):
            raise TypeError("Allow callable must return bool.")

        if ignore is False:
            continue

        filtered_list_values.append(value)

    return filtered_list_values


def validate_parser(
    parser: Base,
):

    if parser and not isinstance(parser, Base):
        raise TypeError("Wrong parser argument type. It must inherit Base parser.")


def is_str_float(value: str) -> bool:
    try:
        float(value)

        return True
    except ValueError:
        return False


def parse_float(
    value: Any,
    decimals: Optional[int] = None,
) -> Optional[float]:

    value = _parse_float(value)

    if value and decimals is not None:
        return round(value, decimals)

    return value


def parse_int(
    value: Any,
) -> Optional[int]:

    if isinstance(value, int):
        return value
    elif isinstance(value, float):
        return int(value)
    elif isinstance(value, str):
        value.strip()

        return _parse_int(value)

    return None


def is_built_in_type(value):
    return isinstance(value, (int, str, float, dict, list, bool, tuple))


def process_item_parser(
    parser,
    data: Any,
    parent_data: Any = None,
    with_parent_data: bool = False,
):
    if parser is None:
        return None

    if isinstance(parser, (str, bool, float, int, list, dict)):
        return parser
    elif isinstance(parser, Base):
        return parser.parse(data, parent_data, with_parent_data)

    if parent_data:
        return parser(parent_data, data)

    return parser(data)
