from typing import Any, Dict, Tuple

from easydata.parsers.base import Base
from easydata.typing import Parser
from easydata.utils import parse

__all__ = (
    "Or",
    "With",
    "Conditional",
    "ConcatText",
    "JoinList",
    "MergeDict",
    "ItemDict",
    "ValueList",
)


class Or(Base):
    _min_len_error_msg = "At least two parsers needs to be passed in order " "to use {}"

    def __init__(
        self,
        *args,
        strict_none: bool = False,
    ):

        self.parsers = args

        self._strict_none = strict_none

        self._validate_fields()

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        for parser in self.parsers:
            value = parse.value_from_parser(
                parser=parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

            if self._strict_none and value is not None:
                return value
            elif not self._strict_none and value:
                return value

    def _validate_fields(self):
        if len(self.parsers) == 1:
            cls_name = self.__class__.__name__
            raise ValueError(self._min_len_error_msg.format(cls_name))


class With(Or):
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parsers = list(self.parsers)

        value = (
            parsers.pop(0)
            .init_config(self.config)
            .parse(
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
            )
        )

        for parser in parsers:
            value = parser.init_config(self.config).parse(value)

        return value


class Conditional(Base):
    def __init__(
        self,
        *args: Tuple[Parser, Parser],
        default: Parser = None,
    ):

        self._condition_parsers = args
        self._default_parser = default

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        for condition_parser_tuple in self._condition_parsers:
            condition_parser, parser = condition_parser_tuple

            condition_value = parse.value_from_parser(
                parser=condition_parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

            if condition_value:
                value = parse.value_from_parser(
                    parser=parser,
                    data=data,
                    parent_data=parent_data,
                    with_parent_data=with_parent_data,
                    config=self.config,
                )

                return value

        if self._default_parser:
            return parse.value_from_parser(
                parser=self._default_parser,
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
                config=self.config,
            )

        return None


class ConcatText(Or):
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


class JoinList(Or):
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


class MergeDict(Or):
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
