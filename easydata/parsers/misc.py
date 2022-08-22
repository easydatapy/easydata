from typing import Any

from easydata.parsers.clause import ItemDict

__all__ = ("StringFormat",)


class StringFormat(ItemDict):
    def __init__(
        self,
        string: str,
        exception_on_non_values: bool = True,
        **kwargs,
    ):

        if not string:
            raise ValueError("string param cannot be emtpy!")

        self._string = string

        kwargs["exception_on_non_values"] = exception_on_non_values

        super().__init__(**kwargs)

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parser_dict = super().parse(
            data=data,
            parent_data=parent_data,
            with_parent_data=with_parent_data,
        )

        return self._string.format(**parser_dict)
