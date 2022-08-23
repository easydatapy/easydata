from typing import Any, Optional, Union

from easytxt import text

from easydata.parsers.text import Text
from easydata.queries.base import QuerySearchBase

__all__ = (
    "Bool",
    "IBool",
)


class Bool(Text):
    def __init__(
        self,
        *args,
        contains: Optional[Union[list, str]] = None,
        ccontains: Optional[Union[list, str]] = None,
        contains_query: Optional[QuerySearchBase] = None,
        has_value: bool = False,
        empty_as_false: bool = True,
        **kwargs,
    ):

        self._contains = ccontains or contains
        self._contains_query = contains_query
        self._has_value = has_value
        self._contains_case = bool(ccontains)
        self._empty_as_false = empty_as_false

        if "default" not in kwargs and empty_as_false:
            kwargs["default"] = False

        super().__init__(
            *args,
            **kwargs,
        )

    def parse_value(
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

        value = super(Bool, self).parse_value(value, data)

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
                source=self.source,
                parent_data=data,
            )

            return contains_values and text.contains(
                text=value,
                keys=contains_values,
            )

        if self._has_value:
            return bool(value)

        return False


class IBool(Bool):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):
        value = super(IBool, self).parse_value(value, data)

        if value is None:
            return value

        return False if value else True
