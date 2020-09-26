from typing import Any, Optional, Union

from easytxt import text

from easydata.parsers.text import Text
from easydata.queries.base import QuerySearch

__all__ = ("Bool",)


class Bool(Text):
    def __init__(
        self,
        *args,
        contains: Optional[Union[list, str]] = None,
        ccontains: Optional[Union[list, str]] = None,
        contains_query: Optional[QuerySearch] = None,
        contains_query_params: Optional[dict] = None,
        contains_query_source: str = "main",
        empty_as_false: bool = True,
        **kwargs,
    ):

        self._contains = ccontains or contains
        self._contains_query = contains_query
        self._contains_query_params = contains_query_params
        self._contains_query_source = contains_query_source
        self._contains_case = bool(ccontains)
        self._empty_as_false = empty_as_false

        if "default" not in kwargs and empty_as_false:
            kwargs["default"] = False

        super().__init__(
            *args,
            **kwargs,
        )

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        if isinstance(value, bool):
            return value

        if isinstance(value, (float, int)):
            return bool(value)

        if isinstance(value, str):
            if "true" == value.lower():
                return True
            elif "false" == value.lower():
                return False

        value = super(Bool, self)._parse_value(value, data)

        if not value:

            return self._default

        if self._contains:
            return self._contains and text.contains(
                text=value,
                keys=self._contains,
                case_sensitive=self._contains_case,
            )

        if self._contains_query:
            contains_values = self._parse_query(
                query=self._contains_query,
                data=data,
                source=self._contains_query_source,
                query_params=self._contains_query_params,
            )

            return contains_values and text.contains(
                text=value,
                keys=contains_values,
            )

        return False
