from typing import Any, Optional, Union

from easydata.parsers.text import Text
from easydata.utils import price

__all__ = (
    "PriceFloat",
    "PriceInt",
    "PriceText",
)


class PriceFloat(Text):
    def __init__(
        self,
        *args,
        decimals: Optional[int] = None,
        min_value: Optional[Union[float, int]] = None,
        max_value: Optional[Union[float, int]] = None,
        **kwargs,
    ):

        self.__decimals = decimals
        self.__min_value = min_value
        self.__max_value = max_value

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _decimals(self):
        if self.__decimals is False or isinstance(self.__decimals, int):
            return self.__decimals

        return self.__decimals or self.config["ED_PRICE_DECIMALS"]

    @property
    def _min_value(self):
        return self.__min_value or self.config["ED_PRICE_MIN_VALUE"]

    @property
    def _max_value(self):
        return self.__max_value or self.config["ED_PRICE_MAX_VALUE"]

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super()._parse_value(
            value=value,
            data=data,
        )

        if value:
            value = price.to_float(
                price_value=value,
                decimals=self._decimals,
            )

            if value is None:
                return None

            return self._process_min_max_value(value)

        return None

    def _process_min_max_value(self, value: float) -> Optional[float]:
        min_value = self._min_value
        max_value = self._max_value

        if min_value and value < min_value:
            return None

        if max_value and value > max_value:
            return None

        return value


class PriceInt(PriceFloat):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super()._parse_value(
            value=value,
            data=data,
        )

        return int(value) if value else None


class PriceText(PriceFloat):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super()._parse_value(
            value=value,
            data=data,
        )

        return str(value) if value else None
