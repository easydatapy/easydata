import json
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, Dict, Iterator, List, Optional, Union

import xmltodict
import yaml
from easytxt.text import replace_chars_by_keys
from pyquery import PyQuery

from easydata.data import DataBag
from easydata.parsers.base import BaseData
from easydata.parsers.data import Data
from easydata.processors.base import BaseProcessor
from easydata.queries.base import QuerySearch
from easydata.queries.re import ReQuery
from easydata.utils import parse

__all__ = (
    "DataProcessor",
    "DataBaseProcessor",
    "DataToPqProcessor",
    "DataJsonToDictProcessor",
    "DataJsonFromQueryToDictProcessor",
    "DataFromIterQueryProcessor",
    "DataYamlToDictProcessor",
    "DataXmlToDictProcessor",
    "DataTextFromReProcessor",
    "DataJsonFromReToDictProcessor",
    "DataFromQueryProcessor",
    "DataVariantsProcessor",
)


class DataBaseProcessor(BaseProcessor, ABC):
    _multi: bool = False

    def __init__(
        self,
        source: str = "main",
        new_source: Optional[str] = None,
        process_source_data=None,
    ):

        self._source = source
        self._new_source = new_source
        self._process_source_data = process_source_data

    def parse(self, data: DataBag) -> Iterator[DataBag]:
        source_data = data[self._source]

        if self._process_source_data:
            source_data = self._process_source_data(source_data)

        transformed_data = self._process_data(source_data)

        if self._multi:
            for iter_transformed_data in transformed_data:
                data_copy = data.copy()

                yield self._transformed_data_to_data(iter_transformed_data, data_copy)
        else:
            yield self._transformed_data_to_data(transformed_data, data)

    def parse_data(self, data=None, **kwargs):
        if data:
            kwargs["main"] = data

        data = DataBag(**kwargs)

        return self.parse(data)

    @abstractmethod
    def _process_data(self, source_data) -> Any:
        pass

    def _transformed_data_to_data(self, transformed_data, data):
        new_source = self._new_source

        if new_source is None:
            original_source = "{}_raw".format(self._source)
            data[original_source] = data[self._source]

            new_source = self._source

        data[new_source] = transformed_data

        return data


class DataProcessor(DataBaseProcessor):
    def _process_data(self, source_data) -> Any:
        return source_data


class DataToPqProcessor(DataBaseProcessor):
    def _process_data(self, source_data: str) -> PyQuery:
        return PyQuery(source_data)


class DataJsonToDictProcessor(DataBaseProcessor):
    def _process_data(self, source_data: str) -> dict:
        return json.loads(source_data)


class DataYamlToDictProcessor(DataBaseProcessor):
    def __init__(
        self,
        *args,
        safe_load: bool = True,
        **kwargs,
    ):

        self._safe_load = safe_load

        super().__init__(*args, **kwargs)

    def _process_data(self, source_data: str) -> dict:
        if self._safe_load:
            return yaml.safe_load(source_data)

        return yaml.load(source_data)


class DataXmlToDictProcessor(DataBaseProcessor):
    def __init__(
        self,
        *args,
        process_namespaces: bool = False,
        namespace_separator: str = ":",
        namespaces: Optional[dict] = None,
        remove_namespaces: Optional[List[str]] = None,
        encoding: Optional[str] = None,
        item_depth: Optional[int] = None,
        strip_whitespace: bool = True,
        attr_prefix: str = "@",
        cdata_key: str = "#text",
        force_cdata: bool = False,
        cdata_separator: str = "",
        force_list: Optional[Any] = None,
        **kwargs,
    ):

        if remove_namespaces:
            namespaces = {n: None for n in remove_namespaces}
            self._process_namespaces = True
        else:
            self._process_namespaces = process_namespaces

        self._namespace_separator = namespace_separator
        self._encoding = encoding
        self._strip_whitespace = strip_whitespace
        self._attr_prefix = attr_prefix
        self._cdata_key = cdata_key
        self._force_cdata = force_cdata
        self._cdata_separator = cdata_separator
        self._namespaces = namespaces
        self._force_list = force_list

        self.__item_depth = item_depth

        super().__init__(*args, **kwargs)

    @property
    def _item_depth(self):
        config_key = "ED_DATA_XML_TO_DICT_ITEM_DEPTH"
        return self.__item_depth or self.config[config_key]

    def _process_data(self, data: Any) -> Any:
        return xmltodict.parse(
            xml_input=data,
            encoding=self._encoding,
            process_namespaces=self._process_namespaces,
            namespace_separator=self._namespace_separator,
            item_depth=self._item_depth,
            strip_whitespace=self._strip_whitespace,
            attr_prefix=self._attr_prefix,
            cdata_key=self._cdata_key,
            force_cdata=self._force_cdata,
            cdata_separator=self._cdata_separator,
            namespaces=self._namespaces,
            force_list=self._force_list,
        )


class DataFromQueryProcessor(DataBaseProcessor):
    def __init__(
        self,
        query: Union[QuerySearch],
        **kwargs,
    ):

        self._query = query

        super().__init__(**kwargs)

    def _process_data(self, data: Any) -> Any:
        return parse.query_search(self._query, data)


class DataFromIterQueryProcessor(DataFromQueryProcessor):
    _multi = True


class DataJsonFromQueryToDictProcessor(DataFromQueryProcessor):
    def process_data(self, data: Any) -> Any:
        jt = super()._process_data(data)

        return json.loads(jt)


class DataTextFromReProcessor(DataBaseProcessor):
    def __init__(
        self,
        *args,
        query,
        dotall=True,
        ignore_case=False,
        bytes_to_string_decode: str = "utf-8",
        replace_keys: Optional[list] = None,
        none_if_empty=False,
        process_value=None,
        **kwargs,
    ):

        self._query = query
        self._dotall = dotall
        self._ignore_case = ignore_case
        self._bytes_to_string_decode = bytes_to_string_decode
        self._replace_keys = replace_keys
        self._none_if_empty = none_if_empty
        self._process_value = process_value

        super().__init__(*args, **kwargs)

    def _process_data(self, source_data: str) -> Any:
        value = ReQuery(
            query=self._query,
            dotall=self._dotall,
            ignore_case=self._ignore_case,
            bytes_to_string_decode=self._bytes_to_string_decode,
        ).get(source_data)

        if not value:
            if self._none_if_empty:
                return None

            error_msg = 'No matches were found for a re queries "{}"'
            raise ValueError(error_msg.format(self._query))

        if self._process_value:
            if isinstance(value, list):
                value = [self._process_value(v) for v in value]
            else:
                value = self._process_value(value)

        if value and self._replace_keys:
            value = replace_chars_by_keys(value, self._replace_keys)

        return value


class DataJsonFromReToDictProcessor(DataTextFromReProcessor):
    def _process_data(self, source_data: str) -> Any:
        value = super()._process_data(source_data)

        if not value:
            return None

        if isinstance(value, list):
            return [json.loads(v) for v in value]

        return json.loads(value)


class DataVariantsProcessor(DataBaseProcessor):
    def __init__(
        self,
        query: Optional[QuerySearch] = None,
        source: str = "main",
        parser: Optional[BaseData] = None,
        key_parser: Optional[BaseData] = None,
        key_query: Optional[QuerySearch] = None,
        **kwargs,
    ):

        if key_parser and key_query:
            error_msg = (
                "key_parser or key_query attributes cannot " "be set at the same time."
            )
            raise AttributeError(error_msg)

        self._query = query
        self._key_parser = key_parser
        self._key_query = key_query

        self.__parser = parser

        super().__init__(
            source=source,
            **kwargs,
        )

    def parse(self, data: DataBag) -> Iterator[DataBag]:
        variants_source = self._new_source or self._source

        for iter_data in super(DataVariantsProcessor, self).parse(data):
            for var_iter_data in parse.variants_data(iter_data, variants_source):
                yield var_iter_data

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def _parser(self) -> Optional[BaseData]:
        return Data(self._query) if self._query else self.__parser

    def _process_data(self, data: Any) -> Dict[Optional[str], Any]:
        variants_data: Dict[Optional[str], Any] = {}

        parser = self._parser

        if parser:
            data = parser.init_config(self.config).parse(data)  # type: ignore

        for data_index, data_info in enumerate(data):
            if self._key_parser:
                variant_group_key = self._key_parser.parse(data_info)
            elif self._key_query:
                variant_group_key = self._key_query.get(data_info)
            else:
                variant_group_key = str(data_index)

            if variant_group_key not in variants_data:
                variants_data[variant_group_key] = []

            variants_data[variant_group_key].append(data_info)

        return variants_data
