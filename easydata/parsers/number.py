from typing import TYPE_CHECKING, Any

from easydata.parsers.base import BaseData
from easydata.parsers.price import BaseNum, BasePriceFloat
from easydata.utils import mix

__all__ = (
    "Float",
    "Int",
    "FloatText",
    "IntText",
    "SearchFloat",
    "SearchInt",
    "SearchFloatText",
    "SearchIntText",
)

# Add BaseData class for type hinting
if TYPE_CHECKING:
    _NumToStrMixin = BaseData
else:
    _NumToStrMixin = object


class NumToStrMixin(_NumToStrMixin):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super().parse_value(value=value, data=data)

        return str(value) if value else None


class NumToIntMixin(_NumToStrMixin):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super().parse_value(value=value, data=data)

        return int(value) if value else None


class DefaultNumConfigMixin:
    @property
    def _decimals_config(self):
        return self.config.get("ED_NUMBER_DECIMALS")

    @property
    def _min_value_config(self):
        return self.config.get("ED_NUMBER_MIN_VALUE")

    @property
    def _max_value_config(self):
        return self.config.get("ED_NUMBER_MAX_VALUE")


class Float(DefaultNumConfigMixin, BaseNum):
    def __init__(
        self,
        *args,
        parse_bool: bool = False,
        **kwargs,
    ):

        self._parse_bool = parse_bool

        super().__init__(
            *args,
            **kwargs,
        )

    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        if self._parse_bool and isinstance(value, bool):
            value = float(value)

        return super().parse_value(value, data)

    def _parse_num_value(self, value: Any):
        return mix.parse_float(
            value=value,
            decimals=self._decimals,
        )


class Int(NumToIntMixin, Float):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        if self._parse_bool and isinstance(value, bool):
            return int(value)

        return super().parse_value(value, data)


class FloatText(NumToStrMixin, Float):
    pass


class IntText(NumToStrMixin, Int):
    pass


class SearchFloat(DefaultNumConfigMixin, BasePriceFloat):
    pass


class SearchInt(NumToIntMixin, SearchFloat):
    pass


class SearchFloatText(NumToStrMixin, SearchFloat):
    pass


class SearchIntText(NumToStrMixin, SearchInt):
    pass
