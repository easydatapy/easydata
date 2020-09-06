from typing import Any
from typing import List as ListType
from typing import Optional, Union

from easytxt import sentences

from easydata.parsers.base import Base, BaseData
from easydata.parsers.data import Data
from easydata.parsers.text import Text
from easydata.parsers.url import Url
from easydata.types import OptionalQuerySearch
from easydata.utils import mix

__all__ = (
    "List",
    "TextList",
    "UrlList",
)


class List(BaseData):
    def __init__(
        self,
        query: OptionalQuerySearch = None,
        parser: Optional[Base] = None,
        unique: bool = True,
        max_num: Optional[int] = None,
        split_key: Optional[str] = None,
        **kwargs,
    ):

        kwargs["query"] = query

        if not parser:
            parser = self._default_parser_obj

        mix.validate_parser(parser)

        self._parser = parser
        self._unique = unique
        self._max_num = max_num
        self._split_key = split_key

        super().__init__(**kwargs)

    @property
    def _default_parser_obj(self) -> Base:
        return Data()

    def _parse_value(self, value: Any, data: Any) -> list:

        if value is None:
            return []

        list_values = self._preprocess_list_values(value)

        parsed_list_values = [
            self._parser.parse(data, lvalue, True) for lvalue in list_values
        ]

        processed_list_values = self._process_list_values(parsed_list_values)

        return self._filter_list_values(processed_list_values)

    def _preprocess_list_values(self, list_values: Any) -> ListType[Any]:

        if isinstance(list_values, (dict, str, int, float)):
            list_values = [list_values]

        if self._split_key:
            list_values = mix.multiply_list_values(
                list_values=list_values,
                split_key=self._split_key,
            )

        return list_values

    def _process_list_values(self, list_values: Any) -> ListType[Any]:

        return list_values

    def _filter_list_values(self, list_values: ListType[str]) -> ListType[Any]:

        if self._unique and list_values:
            list_values = mix.unique_list(list_values)

        if self._max_num and len(list_values) >= self._max_num:
            return list_values[0 : self._max_num]

        return list_values


class TextList(List):
    def __init__(
        self,
        *args,
        allow: Optional[Union[str, ListType[str]]] = None,
        callow: Optional[Union[str, ListType[str]]] = None,
        from_allow: Optional[Union[str, ListType[str]]] = None,
        from_callow: Optional[Union[str, ListType[str]]] = None,
        to_allow: Optional[Union[str, ListType[str]]] = None,
        to_callow: Optional[Union[str, ListType[str]]] = None,
        deny: Optional[Union[str, ListType[str]]] = None,
        cdeny: Optional[Union[str, ListType[str]]] = None,
        multiply_keys: Optional[Union[list, tuple]] = None,
        **kwargs,
    ):

        self._allow = allow
        self._callow = callow
        self._from_allow = from_allow
        self._from_callow = from_callow
        self._to_allow = to_allow
        self._to_callow = to_callow
        self._deny = deny
        self._cdeny = cdeny
        self._multiply_keys = multiply_keys

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _default_parser_obj(self) -> Text:
        return Text()

    def _process_list_values(
        self,
        list_values: Any,
    ) -> ListType[Any]:

        if self._multiply_keys:
            list_values = mix.multiply_list_values(
                list_values=list_values,
                multiply_keys=self._multiply_keys,
            )

        return list_values

    def _filter_list_values(
        self,
        list_values: ListType[str],
    ) -> ListType[str]:

        allow_keys = self._callow or self._allow

        if allow_keys:
            list_values = sentences.allow_contains(
                sentences=list_values,
                keys=allow_keys,
                case_sensitive=bool(self._callow),
            )

        from_allow_keys = self._from_allow or self._from_callow

        if from_allow_keys:
            list_values = sentences.from_allow_contains(
                sentences=list_values,
                keys=from_allow_keys,
                case_sensitive=bool(self._from_callow),
            )

        to_allow_keys = self._to_allow or self._to_callow

        if to_allow_keys:
            list_values = sentences.to_allow_contains(
                sentences=list_values,
                keys=to_allow_keys,
                case_sensitive=bool(self._to_callow),
            )

        deny_keys = self._cdeny or self._deny

        if deny_keys:
            list_values = sentences.deny_contains(
                sentences=list_values,
                keys=deny_keys,
                case_sensitive=bool(self._cdeny),
            )

        return super(TextList, self)._filter_list_values(list_values)


class UrlList(TextList):
    @property
    def _default_parser_obj(self) -> Url:
        return Url()
