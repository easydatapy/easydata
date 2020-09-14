from typing import Any

from easydata.parsers.base import BaseData

__all__ = ("Data",)


class Data(BaseData):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):
        return value
