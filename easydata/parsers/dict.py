from typing import Any
from typing import Dict as TypeDict
from typing import Optional

from easydata.parsers.base import Base, BaseData
from easydata.parsers.bool import Bool
from easydata.parsers.data import Data
from easydata.types import OptionalQuerySearch
from easydata.utils import mix

__all__ = (
    "Dict",
    "BoolDict",
)


class Dict(BaseData):
    def __init__(
        self,
        query: OptionalQuerySearch = None,
        key_parser: Base = None,
        value_parser: Base = None,
        key_query: OptionalQuerySearch = None,
        value_query: OptionalQuerySearch = None,
        ignore_non_values: bool = False,
        **kwargs,
    ):

        self._key_query = key_query
        self._value_query = value_query

        if not key_parser:
            key_parser = self._default_key_parser_obj

        mix.validate_parser(key_parser)

        if not value_parser:
            value_parser = self._default_value_parser_obj

        mix.validate_parser(value_parser)

        self._key_parser = key_parser
        self._value_parser = value_parser
        self._ignore_non_values = ignore_non_values

        super().__init__(
            query=query,
            **kwargs,
        )

    @property
    def _default_key_parser_obj(self) -> Base:
        return Data(self._key_query)

    @property
    def _default_value_parser_obj(self) -> Base:
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
                parsed_key = self._key_parser.parse(data, s_key, True)
                parsed_value = self._value_parser.parse(data, s_value, True)

                values[parsed_key] = parsed_value
        else:
            for s_value in value:
                parsed_key = self._key_parser.parse(data, s_value, True)
                parsed_value = self._value_parser.parse(data, s_value, True)

                values[parsed_key] = parsed_value

        if self._ignore_non_values:
            return {k: v for k, v in values.items() if v}

        return values


class BoolDict(Dict):
    @property
    def _default_value_parser_obj(self) -> Base:
        return Bool(self._value_query)
