from abc import ABC
from typing import List, Optional, Union

from easydata.processors.base import BaseProcessor
from easydata.utils import price, validate

__all__ = (
    "ItemBaseProcessor",
    "ItemKeysMergeIntoListProcessor",
    "ItemKeysMergeProcessor",
    "ItemKeysMergeIntoDictProcessor",
    "ItemValueToStrProcessor",
    "ItemRemoveKeysProcessor",
    "ItemDiscountProcessor",
)


class ItemBaseProcessor(BaseProcessor, ABC):
    pass


class ItemKeysMergeIntoListProcessor(ItemBaseProcessor):
    def __init__(
        self,
        new_item_key: str,
        item_keys: List[str],
        preserve_original=False,
        ignore_none=True,
    ):

        self._new_item_key = new_item_key
        self._item_keys = item_keys
        self._preserve_original = preserve_original
        self._ignore_none = ignore_none

    def parse(self, item: dict) -> dict:
        new_item_value_list = [v for f, v in self._get_item_values(item)]

        item[self._new_item_key] = new_item_value_list

        return item

    def _get_item_values(self, item):
        for item_key in self._item_keys:
            validate.key_in_item(item_key, item)

            value = item[item_key]

            if value is None and self._ignore_none:
                continue

            if not self._preserve_original:
                del item[item_key]

            yield item_key, value


class ItemKeysMergeIntoDictProcessor(ItemKeysMergeIntoListProcessor):
    def parse(self, item: dict) -> dict:
        new_item_value_dict = {f: v for f, v in self._get_item_values(item)}

        item[self._new_item_key] = new_item_value_dict

        return item


class ItemKeysMergeProcessor(ItemKeysMergeIntoListProcessor):
    def __init__(
        self,
        new_item_key: str,
        item_keys: List[str],
        preserve_original=False,
        separator: str = " ",
    ):

        self.separator = separator

        super(ItemKeysMergeProcessor, self).__init__(
            new_item_key=new_item_key,
            item_keys=item_keys,
            preserve_original=preserve_original,
        )

    def parse(self, item: dict) -> dict:
        item = super(ItemKeysMergeProcessor, self).parse(item)

        if not all(isinstance(val, str) for val in item[self._new_item_key]):
            error_msg = (
                "Item value in order to be merged into {} " "has to be of type str!"
            )
            raise TypeError(error_msg.format(self._new_item_key))

        item[self._new_item_key] = self.separator.join(item[self._new_item_key])

        return item


class ItemValueToStrProcessor(ItemBaseProcessor):
    def __init__(
        self,
        item_keys: List[str],
        none_as_empty_string: bool = True,
    ):

        self._item_keys = item_keys
        self._none_as_empty_string = none_as_empty_string

    def parse(self, item: dict) -> dict:
        for item_key in self._item_keys:
            value = item[item_key]

            if isinstance(value, str):
                continue

            if self._none_as_empty_string and value is None:
                item[item_key] = ""
            elif value and isinstance(value, (int, float)):
                item[item_key] = str(value)

        return item


class ItemRemoveKeysProcessor(ItemBaseProcessor):
    def __init__(self, item_keys: List[str]):

        self._item_keys = item_keys

    def parse(self, item: dict) -> dict:
        for item_key in self._item_keys:
            del item[item_key]

        return item


class ItemDiscountProcessor(ItemBaseProcessor):
    def __init__(
        self,
        item_price_key: Optional[str] = None,
        item_sale_price_key: Optional[str] = None,
        item_discount_key: Optional[str] = None,
        decimals: Optional[int] = None,
        no_decimals: Optional[bool] = None,
        remove_item_sale_price_key: Optional[bool] = None,
    ):

        self.__item_price_key = item_price_key
        self.__item_sale_price_key = item_sale_price_key
        self.__item_discount_key = item_discount_key
        self.__decimals = decimals
        self.__no_decimals = no_decimals
        self.__remove_item_sale_price_key = remove_item_sale_price_key

    @property
    def _item_price_key(self):
        config_key = "ED_ITEM_DISCOUNT_ITEM_PRICE_KEY"
        return self.__item_price_key or self.config[config_key]

    @property
    def _item_sale_price_key(self):
        config_key = "ED_ITEM_DISCOUNT_ITEM_SALE_PRICE_KEY"
        return self.__item_sale_price_key or self.config[config_key]

    @property
    def _item_discount_key(self):
        config_key = "ED_ITEM_DISCOUNT_ITEM_DISCOUNT_KEY"
        return self.__item_discount_key or self.config[config_key]

    @property
    def _decimals(self):
        config_key = "ED_ITEM_DISCOUNT_DECIMALS"
        return self.__decimals or self.config[config_key]

    @property
    def _no_decimals(self):
        config_key = "ED_ITEM_DISCOUNT_NO_DECIMALS"
        return self.__no_decimals or self.config[config_key]

    @property
    def _remove_item_sale_price_key(self):
        config_key = "ED_ITEM_DISCOUNT_REMOVE_ITEM_SALE_PRICE_KEY"
        return self.__remove_item_sale_price_key or self.config[config_key]

    def parse(self, item: dict) -> dict:
        item_price = self._get_float_price_value_from_item_by_key(
            item=item,
            item_price_key=self._item_price_key,
        )

        item_sale_price = self._get_float_price_value_from_item_by_key(
            item=item,
            item_price_key=self._item_sale_price_key,
            allow_none=True,
        )

        if not item_sale_price:
            item[self._item_discount_key] = 0
        else:
            item[self._item_discount_key] = price.get_discount(
                price=item_price,
                sale_price=item_sale_price,
                decimals=self._decimals,
                no_decimals=self._no_decimals,
            )

        if self._remove_item_sale_price_key:
            del item[self._item_sale_price_key]

        return item

    def _get_float_price_value_from_item_by_key(
        self,
        item: dict,
        item_price_key: str,
        allow_none: bool = False,
    ) -> Union[float, int]:

        item_price = item[item_price_key]

        if isinstance(item_price, str):
            item_price = price.to_float(item_price)

        validate.price_value_type(
            item_price_key,
            item_price,
            allow_none,
        )

        return item_price if item_price else 0
