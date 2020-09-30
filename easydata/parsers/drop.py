from typing import Any, Optional, Union

from easytxt import text

from easydata.parsers.data import Data
from easydata.parsers.text import Text
from easydata.queries.base import QuerySearch

__all__ = (
    "DropContains",
    "DropEmpty",
)


class DropContains(Text):
    def __init__(
        self,
        *args,
        contains: Optional[Union[list, str]] = None,
        ccontains: Optional[Union[list, str]] = None,
        contains_query: Optional[QuerySearch] = None,
        contains_query_params: Optional[dict] = None,
        contains_query_source: str = "main",
        error_msg: str = "Item dropped due to matched key: {key}",
        **kwargs,
    ):

        self._contains = ccontains or contains
        self._contains_query = contains_query
        self._contains_query_params = contains_query_params
        self._contains_query_source = contains_query_source
        self._contains_case = bool(ccontains)
        self._error_msg = error_msg

        super().__init__(
            *args,
            **kwargs,
        )

    def _exception(self, msg: str):
        return self.config["ED_DROP_ITEM_EXCEPTION"](msg)

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super(DropContains, self)._parse_value(value, data)

        if not value:

            return None

        if self._contains:
            if not isinstance(value, (list, tuple)):
                value = [value]

            for value_key in value:
                if text.contains(
                    text=value_key,
                    keys=self._contains,
                    case_sensitive=self._contains_case,
                ):

                    raise self._exception(self._error_msg.format(key=value_key))

        if self._contains_query:
            contains_values = self._parse_query(
                query=self._contains_query,
                data=data,
                source=self._contains_query_source,
                query_params=self._contains_query_params,
            )

            if not contains_values:
                return None

            if not isinstance(value, (list, tuple)):
                contains_values = [contains_values]

            for contain_value in contains_values:
                if text.contains(
                    text=value,
                    keys=contain_value,
                ):

                    raise self._exception(self._error_msg.format(key=contain_value))

        return None


class DropEmpty(Data):
    def __init__(
        self,
        *args,
        error_msg: str,
        **kwargs,
    ):

        self._error_msg = error_msg

        super().__init__(
            *args,
            **kwargs,
        )

    def _exception(self, msg: str):
        return self.config["ED_DROP_ITEM_EXCEPTION"](msg)

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        if not value:
            raise self._exception(self._error_msg.format(value))

        return value
