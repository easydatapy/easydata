from typing import Union


def key_in_item(
    item_key: str,
    item: dict,
) -> None:

    if item_key not in item:
        error_msg = "Provided item key {} doesnt's exist in item."
        raise KeyError(error_msg.format(item_key))


def price_value_type(
    item_price_key: str,
    price: Union[str, float, None],
    allow_none: bool = False,
) -> None:

    if allow_none and price is None:
        return

    if not isinstance(price, (str, float, int)):
        error_msg = "{} supported types are str, float, int"
        raise ValueError(error_msg.format(item_price_key))
