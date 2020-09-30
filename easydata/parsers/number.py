from typing import Any

from easydata.parsers.price import BasePriceFloat

__all__ = (
    "Float",
    "Int",
    "FloatText",
    "IntText",
)


class Float(BasePriceFloat):
    @property
    def _decimals_config(self):
        return self.config["ED_NUMBER_DECIMALS"]

    @property
    def _min_value_config(self):
        return self.config["ED_NUMBER_MIN_VALUE"]

    @property
    def _max_value_config(self):
        return self.config["ED_NUMBER_MAX_VALUE"]


class Int(Float):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super()._parse_value(value=value, data=data)

        return int(value) if value else None


class FloatText(Float):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super()._parse_value(value=value, data=data)

        return str(value) if value else None


class IntText(Int):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super()._parse_value(value=value, data=data)

        return str(value) if value else None
