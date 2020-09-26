from functools import lru_cache
from typing import Any
from typing import Dict as TypeDict
from typing import List, Optional, Union

from easytxt import sentences

from easydata.parsers.base import Base, BaseData
from easydata.parsers.bool import Bool
from easydata.parsers.data import Data
from easydata.parsers.price import PriceFloat, PriceText
from easydata.parsers.text import Text
from easydata.queries.base import QuerySearch
from easydata.utils import mix

__all__ = (
    "Dict",
    "TextDict",
    "BoolDict",
    "PriceFloatDict",
    "PriceTextDict",
)


class Dict(BaseData):
    def __init__(
        self,
        query: Optional[QuerySearch] = None,
        key_parser: Base = None,
        val_parser: Base = None,
        key_query: Optional[QuerySearch] = None,
        val_query: Optional[QuerySearch] = None,
        ignore_non_values: bool = False,
        ignore_non_keys: bool = True,
        key_normalize: bool = True,
        key_title: bool = False,
        key_uppercase: bool = False,
        key_lowercase: bool = False,
        key_replace_keys: Optional[list] = None,
        key_remove_keys: Optional[list] = None,
        key_split_text_key: Optional[Union[str, tuple]] = None,
        key_split_text_keys: Optional[List[Union[str, tuple]]] = None,
        key_take: Optional[int] = None,
        key_skip: Optional[int] = None,
        key_fix_spaces: bool = True,
        key_allow: Optional[Union[str, List[str]]] = None,
        key_callow: Optional[Union[str, List[str]]] = None,
        key_deny: Optional[Union[str, List[str]]] = None,
        key_cdeny: Optional[Union[str, List[str]]] = None,
        key_default: Optional[str] = None,
        **kwargs,
    ):

        self._key_text_parser_properties = {
            "normalize": key_normalize,
            "title": key_title,
            "uppercase": key_uppercase,
            "lowercase": key_lowercase,
            "replace_keys": key_replace_keys,
            "remove_keys": key_remove_keys,
            "split_key": key_split_text_key,
            "split_keys": key_split_text_keys,
            "take": key_take,
            "skip": key_skip,
            "fix_spaces": key_fix_spaces,
        }

        self._key_query = key_query
        self._value_query = val_query
        self._ignore_non_values = ignore_non_values
        self._ignore_non_keys = ignore_non_keys
        self._key_allow = key_allow
        self._key_callow = key_callow
        self._key_deny = key_deny
        self._key_cdeny = key_cdeny
        self._key_default = key_default

        self.__key_parser = key_parser
        self.__key_parser_obj = None

        self.__value_parser = val_parser
        self.__value_parser_obj = None

        super().__init__(
            query=query,
            **kwargs,
        )

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def _key_parser(self):
        # Initialize and validate key parser
        key_parser_obj = self.__key_parser or self._default_key_parser_obj

        mix.validate_parser(key_parser_obj)

        key_parser_obj.init_config(self.config)

        return key_parser_obj

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def _value_parser(self):
        # Initialize and validate value parser
        value_parser_obj = self.__value_parser or self._default_value_parser_obj

        mix.validate_parser(value_parser_obj)

        value_parser_obj.init_config(self.config)

        return value_parser_obj

    @property
    def _default_key_parser_obj(self):
        return Text(query=self._key_query, **self._key_text_parser_properties)

    @property
    def _default_value_parser_obj(self):
        return Data(self._value_query)

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ) -> dict:

        if not value:
            return {}

        values: TypeDict[Optional[str], Any] = {}

        if isinstance(value, dict):
            for s_key, s_value in value.items():
                parsed_key = self._key_parser.parse(data, s_key, True)  # type: ignore
                parsed_value = self._value_parser.parse(  # type: ignore
                    data, s_value, True
                )

                values[parsed_key] = parsed_value
        else:
            for s_value in value:
                parsed_key = self._key_parser.parse(data, s_value, True)  # type: ignore
                parsed_value = self._value_parser.parse(  # type: ignore
                    data, s_value, True
                )

                values[parsed_key] = parsed_value

        if self._ignore_non_values:
            values = {k: v for k, v in values.items() if v is not None}

        values = self._filter_dict_items(values)

        return values

    def _filter_dict_items(self, values: dict) -> dict:
        if self._ignore_non_keys:
            values = {k: v for k, v in values.items() if k is not None}

        allow_keys = self._key_callow or self._key_allow

        if allow_keys and values:
            item_keys = sentences.allow_contains(
                sentences=list(values.keys()),
                keys=allow_keys,
                case_sensitive=bool(self._key_callow),
            )

            values = {k: v for k, v in values.items() if k in item_keys}

        deny_keys = self._key_cdeny or self._key_deny

        if deny_keys and values:
            item_keys = sentences.deny_contains(
                sentences=list(values.keys()),
                keys=deny_keys,
                case_sensitive=bool(self._key_cdeny),
            )

            values = {k: v for k, v in values.items() if k in item_keys}

        if self._key_default and values:
            values = {k or self._key_default: v for k, v in values.items()}

        return values


class TextDict(Dict):
    def __init__(
        self,
        *args,
        val_normalize: bool = True,
        val_title: bool = False,
        val_uppercase: bool = False,
        val_lowercase: bool = False,
        val_replace_keys: Optional[list] = None,
        val_remove_keys: Optional[list] = None,
        val_split_text_key: Optional[Union[str, tuple]] = None,
        val_split_text_keys: Optional[List[Union[str, tuple]]] = None,
        val_take: Optional[int] = None,
        val_skip: Optional[int] = None,
        val_fix_spaces: bool = True,
        val_allow: Optional[Union[str, List[str]]] = None,
        val_callow: Optional[Union[str, List[str]]] = None,
        val_deny: Optional[Union[str, List[str]]] = None,
        val_cdeny: Optional[Union[str, List[str]]] = None,
        **kwargs,
    ):

        self._val_allow = val_allow
        self._val_callow = val_callow
        self._val_deny = val_deny
        self._val_cdeny = val_cdeny

        self._value_text_parser_properties = {
            "normalize": val_normalize,
            "title": val_title,
            "uppercase": val_uppercase,
            "lowercase": val_lowercase,
            "replace_keys": val_replace_keys,
            "remove_keys": val_remove_keys,
            "split_key": val_split_text_key,
            "split_keys": val_split_text_keys,
            "take": val_take,
            "skip": val_skip,
            "fix_spaces": val_fix_spaces,
        }

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _default_value_parser_obj(self):
        return Text(
            query=self._value_query,
            **self._value_text_parser_properties,
        )

    def _filter_dict_items(self, values: dict) -> dict:
        values = super()._filter_dict_items(values)

        allow_values = self._val_callow or self._val_allow

        if allow_values and values:
            item_values = sentences.allow_contains(
                sentences=list(values.values()),
                keys=allow_values,
                case_sensitive=bool(self._val_callow),
            )

            values = {k: v for k, v in values.items() if v in item_values}

        deny_values = self._val_cdeny or self._val_deny

        if deny_values and values:
            item_values = sentences.deny_contains(
                sentences=list(values.values()),
                keys=deny_values,
                case_sensitive=bool(self._val_cdeny),
            )

            values = {k: v for k, v in values.items() if v in item_values}

        return values


class BoolDict(TextDict):
    def __init__(
        self,
        *args,
        val_contains: Optional[Union[list, str]] = None,
        val_ccontains: Optional[Union[list, str]] = None,
        val_contains_query: Optional[QuerySearch] = None,
        val_contains_query_params: Optional[dict] = None,
        val_contains_query_source: str = "data",
        val_empty_as_false: bool = True,
        **kwargs,
    ):

        self._value_bool_parser_properties = {
            "contains": val_contains,
            "ccontains": val_ccontains,
            "contains_query": val_contains_query,
            "contains_query_params": val_contains_query_params,
            "contains_query_source": val_contains_query_source,
            "empty_as_false": val_empty_as_false,
        }

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _default_value_parser_obj(self):
        return Bool(
            query=self._value_query,
            **self._value_bool_parser_properties,
            **self._value_text_parser_properties,
        )


class PriceFloatDict(TextDict):
    def __init__(
        self,
        *args,
        val_decimals: Optional[int] = None,
        val_min_value: Optional[Union[float, int]] = None,
        val_max_value: Optional[Union[float, int]] = None,
        **kwargs,
    ):

        self._value_price_parser_properties = {
            "decimals": val_decimals,
            "min_value": val_min_value,
            "max_value": val_max_value,
        }

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _default_value_parser_obj(self):
        return PriceFloat(
            query=self._value_query,
            **self._value_price_parser_properties,
            **self._value_text_parser_properties,
        )


class PriceTextDict(PriceFloatDict):
    @property
    def _default_value_parser_obj(self):
        return PriceText(
            query=self._value_query,
            **self._value_price_parser_properties,
            **self._value_text_parser_properties,
        )
