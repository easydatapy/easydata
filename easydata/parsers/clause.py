from typing import Any, Callable, Optional

from easydata.parsers.base import Base
from easydata.typing import Parser
from easydata.utils import mix, parse

__all__ = (
    "OR",
    "WITH",
    "SWITCH",
    "IF",
)


class OR(Base):
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


class WITH(OR):
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


class SWITCH(Base):
    def __init__(
        self,
        parser: Parser,
        *cases,
        default: Any = None,
    ):

        self._parser = parser
        self._cases = cases
        self._default = default

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parser_data = {
            "data": data,
            "parent_data": parent_data,
            "with_parent_data": with_parent_data,
            "config": self.config,
        }

        value = parse.value_from_parser(
            parser=self._parser,
            **parser_data,
        )

        for case in self._cases:
            if not isinstance(case, tuple):
                raise TypeError(
                    "Case must be of type tuple (<case-value>, <return-parser>)",
                )

            case_value, return_parser = case

            if case_value == value:
                if mix.is_built_in_type(return_parser):
                    return return_parser

                return parse.value_from_parser(
                    parser=return_parser,
                    **parser_data,
                )

        if self._default:
            if mix.is_built_in_type(self._default):
                return self._default

            return parse.value_from_parser(
                parser=self._default,
                **parser_data,
            )

        return None


class IF(Base):
    def __init__(
        self,
        if_parser: Parser,
        then_parser: Any,
        else_parser: Optional[Any] = None,
        condition: Optional[Callable] = None,
    ):

        self._if_parser = if_parser
        self._then_parser = then_parser
        self._else_parser = else_parser
        self._condition = condition

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parser_data = {
            "data": data,
            "parent_data": parent_data,
            "with_parent_data": with_parent_data,
            "config": self.config,
        }

        condition_value = parse.value_from_parser(
            parser=self._if_parser,
            **parser_data,
        )

        if self._has_condition(condition_value):
            if mix.is_built_in_type(self._then_parser):
                return self._then_parser

            value = parse.value_from_parser(
                parser=self._then_parser,
                **parser_data,
            )

            return value

        if self._else_parser:
            if mix.is_built_in_type(self._else_parser):
                return self._else_parser

            return parse.value_from_parser(
                parser=self._else_parser,
                **parser_data,
            )

        return None

    def _has_condition(self, value):
        if self._condition:
            return self._condition(value)

        return value
