from typing import Any, Dict

from easydata.parsers.base import Base
from easydata.parsers.clause import OR
from easydata.typing import Parser
from easydata.utils import parse

__all__ = (
    "ConcatText",
    "JoinList",
    "MergeDict",
    "ItemDict",
    "ValueList",
    "StringFormat",
)


class ConcatText(OR):
    def __init__(
        self,
        *args: Parser,
        separator: str = " ",
    ):

        self._separator = separator

        super().__init__(*args)

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        values = []

        for parser in self.parsers:
            value = parse.value_from_parser(
                parser=parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

            if value is None:
                continue

            if not isinstance(value, str):
                error_msg = "Value returned from {} must be type of str!"
                raise TypeError(error_msg.format(type(parser).__name__))

            values.append(value)

        return self._separator.join(values)


class JoinList(OR):
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        values = []

        for parser in self.parsers:
            value = parse.value_from_parser(
                parser=parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

            if not value:
                continue

            if not isinstance(value, list):
                error_msg = "Value returned from {} must be type of list!"
                raise TypeError(error_msg.format(type(parser).__name__))

            values += value

        return values


class MergeDict(OR):
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        joined_dictionary: Dict[Any, Any] = {}

        for parser in self.parsers:
            value = parse.value_from_parser(
                parser=parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

            if not value:
                continue

            if not isinstance(value, dict):
                error_msg = "Value returned from {} must be type of dict!"
                raise TypeError(error_msg.format(type(parser).__name__))

            joined_dictionary = {**joined_dictionary, **value}

        return joined_dictionary


class ItemDict(Base):
    def __init__(
        self,
        ignore_non_values: bool = False,
        exception_on_non_values: bool = False,
        **kwargs,
    ):

        self._ignore_non_values = ignore_non_values
        self._exception_on_non_values = exception_on_non_values
        self._parser_dict = kwargs

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parser_dict = {}

        for name, parser in self._parser_dict.items():
            value = parse.value_from_parser(
                parser=parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

            if self._ignore_non_values and value is None:
                continue

            if self._exception_on_non_values and value is None:
                error_msg = "Value for dict key %s cannot be emtpy!"

                raise ValueError(error_msg % name)

            parser_dict[name] = value

        return parser_dict


class ValueList(Base):
    def __init__(
        self,
        *args: Parser,
        ignore_non_values: bool = True,
    ):

        self._parser_list = args
        self._ignore_non_values = ignore_non_values

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parser_list = []

        for parser in self._parser_list:
            value = parse.value_from_parser(
                parser=parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

            if self._ignore_non_values and value is None:
                continue

            parser_list.append(value)

        return parser_list


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
