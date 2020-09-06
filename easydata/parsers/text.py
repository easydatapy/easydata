from typing import Any, List, Optional, Union

from easytxt import parse_string, text

from easydata.parsers import BaseData

__all__ = ("Text",)


class Text(BaseData):
    def __init__(
        self,
        *args,
        normalize: bool = True,
        capitalize: bool = False,
        title: bool = False,
        uppercase: bool = False,
        lowercase: bool = False,
        replace_keys: Optional[list] = None,
        remove_keys: Optional[list] = None,
        split_key: Optional[Union[str, tuple]] = None,
        split_keys: Optional[List[Union[str, tuple]]] = None,
        take: Optional[int] = None,
        skip: Optional[int] = None,
        text_num_to_numeric: bool = False,
        language: Optional[str] = None,
        fix_spaces: bool = True,
        escape_new_lines: bool = True,
        new_line_replacement: str = " ",
        add_stop: Optional[Union[bool, str]] = None,
        separator: str = " ",
        index: Optional[int] = None,
        **kwargs,
    ):

        self._normalize = normalize
        self._capitalize = capitalize
        self._title = title
        self._uppercase = uppercase
        self._lowercase = lowercase
        self._replace_keys = replace_keys
        self._remove_keys = remove_keys
        self._split_key = split_key
        self._split_keys = split_keys
        self._take = take
        self._skip = skip
        self._text_num_to_numeric = text_num_to_numeric
        self._fix_spaces = fix_spaces
        self._escape_new_lines = escape_new_lines
        self._new_line_replacement = new_line_replacement
        self._add_stop = add_stop
        self._separator = separator
        self._index = index

        self.__language = language

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _language(self):
        return self.__language or self.config["ED_LANGUAGE"]

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super(Text, self)._parse_value(
            value=value,
            data=data,
        )

        if isinstance(value, (list, tuple)):

            value = [text.to_str(v) for v in value if v]

            if not value:
                return None

            if self._index is not None:
                value = value[self._index]
            else:
                value = self._separator.join(value)

        value = parse_string(
            raw_text=value,
            normalize=self._normalize,
            title=self._title,
            capitalize=self._capitalize,
            uppercase=self._uppercase,
            lowercase=self._lowercase,
            replace_keys=self._replace_keys,
            remove_keys=self._remove_keys,
            split_key=self._split_key,
            split_keys=self._split_keys,
            take=self._take,
            skip=self._skip,
            text_num_to_numeric=self._text_num_to_numeric,
            language=self._language,
            fix_spaces=self._fix_spaces,
            escape_new_lines=self._escape_new_lines,
            new_line_replacement=self._new_line_replacement,
            add_stop=self._add_stop,
        )

        return value if value else None
