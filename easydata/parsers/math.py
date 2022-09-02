from typing import Any

from easydata.parsers.base import BaseData

__all__ = ("Count",)


class Count(BaseData):
    def __init__(
        self,
        *args,
        count_bool: bool = False,
        none_as_zero: bool = False,
        **kwargs,
    ):

        self._count_bool = count_bool
        self._none_as_zero = none_as_zero

        super().__init__(
            *args,
            **kwargs,
        )

    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        if isinstance(value, bool) and self._count_bool:
            return 1 if value is True else 0

        if value is None and self._none_as_zero:
            return 0

        return len(value)
