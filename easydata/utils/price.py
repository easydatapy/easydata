from typing import Optional, Union

from easytxt import text
from price_parser import Price


def to_float(
    price_value: Union[str, int, float],
    decimals: Union[int, bool] = 2,
):

    price_str_value: str = text.to_str(price_value)

    price = Price.fromstring(price=price_str_value).amount_float

    if not price:
        return price

    return round(price, decimals) if decimals is not None else price


def to_string(
    price_value: Union[str, int, float],
    decimals: Union[int, bool] = 2,
):

    price = to_float(price_value=price_value, decimals=decimals)
    return str(price) if price else price


def get_discount(
    price: float,
    sale_price: float,
    decimals: int = 2,
    no_decimals: bool = False,
) -> Union[float, int]:

    if no_decimals:
        decimals = 0

    discount = 1 - (sale_price / price)
    discount = discount * 100
    discount = round(discount, decimals)

    if no_decimals:
        discount = int(discount)

    return discount


def process_min_max_value(
    value: Union[float, int],
    min_value: Optional[Union[float, int]] = None,
    max_value: Optional[Union[float, int]] = None,
) -> Optional[Union[float, int]]:

    if min_value and value < min_value:
        return None

    if max_value and value > max_value:
        return None

    return value
