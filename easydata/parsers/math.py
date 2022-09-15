from typing import Any
from typing import List as ListType
from typing import Optional

from easydata.parsers.base import BaseData
from easydata.parsers.list import List
from easydata.utils import mix

__all__ = (
    "Count",
    "Avg",
    "AvgInt",
)


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


class Avg(List):
    def __init__(
        self,
        *args,
        decimals: Optional[int] = None,
        **kwargs,
    ):

        self._decimals = decimals

        super().__init__(
            *args,
            **kwargs,
        )

    def parse_value(
        self,
        value: Any,
        data: Any,
    ) -> Any:

        list_values = super().parse_value(value, data)

        if not list_values:
            return None

        list_values = self._filter_avg_list_values(list_values)

        if not list_values:
            return None

        total_count = len(list_values)

        avg_price = sum(list_values) / total_count

        return mix.parse_float(avg_price, decimals=self._decimals)

    def _filter_avg_list_values(self, list_values: ListType[Any]):
        return [mix.parse_float(v) for v in list_values if v]


class AvgInt(Avg):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super().parse_value(value, data)

        return int(value) if value else None
