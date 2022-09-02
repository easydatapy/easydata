from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from easydata.parsers.text import Str
from easydata.utils import price

__all__ = (
    "BaseNum",
    "BasePriceFloat",
    "PriceFloat",
    "PriceInt",
    "PriceText",
)


class BaseNum(Str, ABC):
    def __init__(
        self,
        *args,
        decimals: Optional[int] = None,
        min_value: Optional[Union[float, int]] = None,
        max_value: Optional[Union[float, int]] = None,
        normalize: bool = False,
        **kwargs,
    ):

        self.__decimals = decimals
        self.__min_value = min_value
        self.__max_value = max_value

        kwargs["normalize"] = normalize

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _decimals(self):
        if isinstance(self.__decimals, int):
            return self.__decimals

        decimals = self.__decimals or self._decimals_config

        return decimals if isinstance(decimals, int) else None

    @property
    def _min_value(self):
        return self.__min_value or self._min_value_config

    @property
    def _max_value(self):
        return self.__max_value or self._max_value_config

    @property
    def _decimals_config(self):
        return None

    @property
    def _min_value_config(self):
        return None

    @property
    def _max_value_config(self):
        return None

    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super().parse_value(value=value, data=data)

        if value is None:
            return None

        value = self._parse_num_value(value)

        if value is None:
            return None

        return price.process_min_max_value(
            value,
            min_value=self._min_value,
            max_value=self._max_value,
        )

    @abstractmethod
    def _parse_num_value(self, value: Any):
        pass


class BasePriceFloat(BaseNum, ABC):
    def __init__(
        self,
        *args,
        currency_hint: Optional[str] = None,
        decimal_separator: Optional[str] = None,
        **kwargs,
    ):

        self._currency_hint = currency_hint
        self._decimal_separator = decimal_separator

        super().__init__(
            *args,
            **kwargs,
        )

    def _parse_num_value(self, value: Any):
        return price.to_float(
            price_value=value,
            decimals=self._decimals,
            currency_hint=self._currency_hint,
            decimal_separator=self._decimal_separator,
        )


class PriceFloat(BasePriceFloat):
    @property
    def _decimals_config(self) -> Optional[int]:
        return self.config.get("ED_PRICE_DECIMALS")

    @property
    def _min_value_config(self) -> Optional[int]:
        return self.config.get("ED_PRICE_MIN_VALUE")

    @property
    def _max_value_config(self) -> Optional[int]:
        return self.config.get("ED_PRICE_MAX_VALUE")


class PriceInt(PriceFloat):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super().parse_value(value=value, data=data)

        return None if value is None else int(value)


class PriceText(PriceFloat):
    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super().parse_value(value=value, data=data)

        return None if value is None else str(value)
