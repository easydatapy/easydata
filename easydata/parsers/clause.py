from typing import Any, Dict

from easydata.parsers.base import Base

__all__ = (
    "Union",
    "With",
    "JoinText",
    "JoinList",
    "JoinDict",
    "ItemDict",
    "ItemList",
)


class Union(Base):
    _min_len_error_msg = "At least two parsers needs to be passed in order " "to use {}"

    def __init__(
        self,
        *kwargs,
    ):

        self.parsers = kwargs

        self._validate_fields()

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        for parser in self.parsers:
            value = parser.parse(
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
            )

            if value is not None:
                return value

    def _validate_fields(self):
        if len(self.parsers) == 1:
            cls_name = self.__class__.__name__
            raise ValueError(self._min_len_error_msg.format(cls_name))


class With(Union):
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parsers = list(self.parsers)

        value = parsers.pop(0).parse(
            data=data,
            parent_data=parent_data,
            with_parent_data=with_parent_data,
        )

        for parser in parsers:
            value = parser.parse(value)

        return value


class JoinText(Union):
    def __init__(
        self,
        *args,
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
            value = parser.parse(
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
            )

            if value is None:
                continue

            if not isinstance(value, str):
                error_msg = "Value returned from {} must be type of str!"
                raise TypeError(error_msg.format(parser.__class__.name))

            values.append(value)

        return self._separator.join(values)


class JoinList(Union):
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        values = []

        for parser in self.parsers:
            value = parser.parse(
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
            )

            if not value:
                continue

            if not isinstance(value, list):
                error_msg = "Value returned from {} must be type of list!"
                raise TypeError(error_msg.format(parser.__class__.name))

            values += value

        return values


class JoinDict(Union):
    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        joined_dictionary: Dict[Any, Any] = {}

        for parser in self.parsers:
            value = parser.parse(
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
            )

            if not value:
                continue

            if not isinstance(value, dict):
                error_msg = "Value returned from {} must be type of dict!"
                raise TypeError(error_msg.format(parser.__class__.name))

            joined_dictionary = {**joined_dictionary, **value}

        return joined_dictionary


class ItemDict(Base):
    def __init__(
        self,
        ignore_non_values: bool = False,
        **kwargs,
    ):

        self._ignore_non_values = ignore_non_values
        self._parser_dict = kwargs

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parser_dict = {}

        for name, parser in self._parser_dict.items():
            value = parser.parse(
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
            )

            if self._ignore_non_values and value is None:
                continue

            parser_dict[name] = value

        return parser_dict


class ItemList(Base):
    def __init__(
        self,
        *kwargs,
        ignore_non_values: bool = True,
    ):

        self._parser_list = kwargs
        self._ignore_non_values = ignore_non_values

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        parser_list = []

        for parser in self._parser_list:
            value = parser.parse(
                data=data,
                parent_data=parent_data,
                with_parent_data=with_parent_data,
            )

            if self._ignore_non_values and value is None:
                continue

            parser_list.append(value)

        return parser_list
