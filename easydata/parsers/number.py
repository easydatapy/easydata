from typing import TYPE_CHECKING, Any, Optional

from easydata.parsers.base import BaseData
from easydata.parsers.price import BaseNum, BasePriceFloat
from easydata.utils import mix

__all__ = (
    "SFloat",
    "SInt",
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


class SFloat(BaseData):
    def __init__(
        self,
        *args,
        decimals: Optional[int] = None,
        **kwargs,
    ):

        self._decimals = decimals

        super().__init__(*args, **kwargs)

    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        if value is None:
            return None

        return mix.parse_float(
            value=value,
            decimals=self._decimals,
        )


class SInt(BaseData):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        return mix.parse_int(value)


class Float(DefaultNumConfigMixin, BaseNum):
    def __init__(
        self,
        *args,
        parse_bool: bool = True,
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

        if isinstance(value, bool):
            return float(value) if self._parse_bool else None

        return super().parse_value(value, data)

    def _parse_num_value(self, value: Any):
        return mix.parse_float(
            value=value,
            decimals=self._decimals,
        )


class Int(BaseNum):
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

        if isinstance(value, bool):
            return int(value) if self._parse_bool else None

        return super().parse_value(value, data)

    def _parse_num_value(self, value: Any):
        return mix.parse_int(value=value)


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
