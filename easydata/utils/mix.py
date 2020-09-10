from typing import Any, Callable, List, Optional, Union

from easytxt.text import to_list
from pyquery import PyQuery

from easydata.config.loader import ConfigLoader
from easydata.data import DataBag
from easydata.parsers.base import Base
from easydata.processors.base import BaseProcessor


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
) -> Any:

    for processor in processors:
        if isinstance(processor, BaseProcessor):
            value = processor.parse(value)
        else:
            value = processor(value)

    return value


def extract_attr_names_from_obj(obj: object, attr_prefix: str):

    attr_names = []

    for attr_name in dir(obj):
        if attr_name.startswith(attr_prefix + "_"):
            attr_names.append(attr_name)

    return attr_names


def iter_attr_data_from_obj(
    obj: object, attr_prefix: str, preserve_prefix: bool = False
):

    attr_name = extract_attr_names_from_obj(obj=obj, attr_prefix=attr_prefix)

    for attr_name in attr_name:
        attr_value = getattr(obj, attr_name)

        if not preserve_prefix:
            attr_name = attr_name.lstrip(attr_prefix).lstrip("_")

        yield attr_name, attr_value


def make_variant_data_copy(
    data: DataBag,
    variant_data: Union[list, dict],
    variant_key: Optional[str] = None,
    variants_name: str = "variants",
    variant_name: str = "variant",
    variants_key_name: str = "variants_key",
):

    data_copy = data.copy()

    data_copy[variants_name] = variant_data
    data_copy[variant_name] = variant_data[0]

    if variant_key:
        data_copy[variants_key_name] = variant_key

    return data_copy


def multiply_list_values(
    list_values: list,
    split_key: Optional[str] = None,
    multiply_keys: Optional[Union[list, tuple]] = None,
) -> list:

    new_all_list_values = []

    for list_value in list_values:
        if not list_value:
            continue

        new_list_values = to_list(
            value=list_value,
            split_key=split_key,
            multiply_keys=multiply_keys,
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
        raise TypeError("Wrong parser argument type. It must inherit BaseParser.")
