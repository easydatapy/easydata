from typing import Any, List, Optional, Union

from easytxt.text import to_list
from pyquery import PyQuery

from easydata.data import DataBag
from easydata.default import Config
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
    config: Config,
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


def extract_item_attr_names_from_cls(cls, preserve_item_prefix=False):
    attr_names = []

    for attr_name in dir(cls):
        if attr_name.startswith("item_"):
            if preserve_item_prefix:
                attr_names.append(attr_name)
            else:
                attr_names.append(attr_name.lstrip("item").lstrip("_"))

    return attr_names


def iter_item_attr_data_from_cls(cls):
    for attr_name in extract_item_attr_names_from_cls(cls, True):
        yield attr_name, getattr(cls, attr_name)


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


def validate_parser(
    parser: Base,
):

    if parser and not isinstance(parser, Base):
        raise TypeError("Wrong parser argument type. It must inherit BaseParser.")
