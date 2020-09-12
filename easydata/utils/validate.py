from typing import Any, Optional, Union

from easydata.data import DataBag


def key_in_item(
    item_key: str,
    item: dict,
) -> None:

    if item_key not in item:
        error_msg = "Provided item key {} does not exist in item."
        raise KeyError(error_msg.format(item_key))


def price_value_type(
    item_price_key: str,
    price: Union[str, float, int, None],
    allow_none: bool = False,
) -> None:

    if allow_none and price is None:
        return

    if not isinstance(price, (str, float, int)):
        error_msg = "{} supported types are str, float, int"
        raise ValueError(error_msg.format(item_price_key))


def if_data_bag_with_source(
    data: Any,
    source: Optional[str] = None,
):
    if isinstance(data, DataBag) and not source:
        raise AttributeError("data of type DataBag needs also source attribute value")
