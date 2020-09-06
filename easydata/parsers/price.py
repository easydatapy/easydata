from typing import Any, Optional

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
        **kwargs,
    ):

        self._decimals = decimals

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def decimals(self):
        if self._decimals is False or isinstance(self._decimals, int):
            return self._decimals

        return self._decimals or self.config["ED_PRICE_DECIMALS"]

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
            return price.to_float(
                price_value=value,
                decimals=self.decimals,
            )

        return None


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
