import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import xmltodict
from pyquery import PyQuery

from easydata.data import DataBag
from easydata.parsers.base import BaseData
from easydata.processors.base import BaseProcessor
from easydata.queries.base import QuerySearch
from easydata.utils import parse

__all__ = (
    "DataProcessor",
    "DataBaseProcessor",
    "DataToPqProcessor",
    "DataJsonToDictProcessor",
    "DataJsonFromQueryToDictProcessor",
    "DataTextFromReProcessor",
    "DataJsonFromReToDictProcessor",
    "DataFromQueryProcessor",
    "DataVariantProcessor",
)


class DataBaseProcessor(BaseProcessor, ABC):
    def __init__(
        self,
        source: str = "data",
        new_source: Optional[str] = None,
        process_source_data=None,
    ):

        self.source = source
        self.new_source = new_source
        self.process_source_data = process_source_data

    def parse(self, data: DataBag) -> DataBag:
        new_source = self.new_source

        source_data = data[self.source]

        if self.process_source_data:
            source_data = self.process_source_data(source_data)

        trans_data = self.process_data(source_data)

        if new_source is None:
            original_source = "{}_raw".format(self.source)
            data[original_source] = data[self.source]

            new_source = self.source

        data[new_source] = trans_data

        return data

    def parse_data(self, data=None, **kwargs):
        if data:
            kwargs["data"] = data

        data = DataBag(self, **kwargs)

        return self.parse(data)

    @abstractmethod
    def process_data(self, source_data) -> Any:
        pass


class DataProcessor(DataBaseProcessor):
    def process_data(self, source_data) -> Any:
        return source_data


class DataToPqProcessor(DataBaseProcessor):
    def process_data(self, source_data: str) -> PyQuery:
        return PyQuery(source_data)


class DataJsonToDictProcessor(DataBaseProcessor):
    def process_data(self, source_data: str) -> PyQuery:
        return json.loads(source_data)


class DataXmlToDictProcessor(DataBaseProcessor):
    def __init__(
        self,
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
        self._item_depth = item_depth
        self._strip_whitespace = strip_whitespace
        self._attr_prefix = attr_prefix
        self._cdata_key = cdata_key
        self._force_cdata = force_cdata
        self._cdata_separator = cdata_separator
        self._namespaces = namespaces
        self._force_list = force_list

        super(DataXmlToDictProcessor, self).__init__(**kwargs)

    @property
    def item_depth(self):
        config_key = "ED_DATA_XML_TO_DICT_ITEM_DEPTH"
        return self._item_depth or self.config[config_key]

    def process_data(self, data: Any) -> Any:
        return xmltodict.parse(
            xml_input=data,
            encoding=self._encoding,
            process_namespaces=self._process_namespaces,
            namespace_separator=self._namespace_separator,
            item_depth=self.item_depth,
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
        query: Union[List[QuerySearch], QuerySearch],
        **kwargs,
    ):

        if isinstance(query, QuerySearch):
            self.query = [query]

        super(DataFromQueryProcessor, self).__init__(**kwargs)

    def process_data(self, data: Any) -> Any:
        return parse.query_search(self.query, data)


class DataJsonFromQueryToDictProcessor(DataFromQueryProcessor):
    def process_data(self, data: Any) -> Any:
        jt = super(DataJsonFromQueryToDictProcessor, self).process_data(data)

        return json.loads(jt)


class DataTextFromReProcessor(DataBaseProcessor):
    def __init__(
        self,
        re_query,
        multi=False,
        dotall=True,
        none_if_empty=False,
        process_value=None,
        **kwargs,
    ):

        self.re_query = re_query
        self.multi = multi
        self.dotall = dotall
        self.none_if_empty = none_if_empty
        self.process_value = process_value

        super(DataTextFromReProcessor, self).__init__(**kwargs)

    def process_data(self, source_data: str) -> Any:
        results = re.findall(self.re_query, source_data, re.DOTALL)

        if not results:
            if self.none_if_empty:
                return None

            error_msg = 'No matches were found for a re queries "{}"'
            raise ValueError(error_msg.format(self.re_query))

        if self.process_value:
            results = [self.process_value(result) for result in results]

        return results if self.multi else results[0]


class DataJsonFromReToDictProcessor(DataTextFromReProcessor):
    def process_data(self, source_data: str) -> Any:
        res = super(DataJsonFromReToDictProcessor, self).process_data(source_data)

        if not res:
            return None

        if self.multi:
            return [json.loads(result) for result in res]

        return json.loads(res)


class DataVariantProcessor(DataBaseProcessor):
    def __init__(
        self,
        source: str = "data",
        parser: Optional[BaseData] = None,
        variant_parser: Optional[BaseData] = None,
        query: Optional[QuerySearch] = None,
        variant_query: Optional[QuerySearch] = None,
        multi_values: bool = False,
        with_variant_values: bool = True,
        variant_values_lower: bool = True,
        **kwargs,
    ):

        if variant_parser and variant_query:
            error_msg = (
                "variant_query or variant_parser attributes cannot "
                "be set at the same time."
            )
            raise AttributeError(error_msg)

        kwargs["source"] = source

        if "new_source" not in kwargs:
            kwargs["new_source"] = "{}_variants".format(kwargs["source"])

        self.parser = parser
        self.variant_parser = variant_parser
        self.query = query
        self.variant_query = variant_query
        self.multi_values = multi_values
        self.with_variant_values = with_variant_values
        self.variant_values_lower = variant_values_lower

        super(DataVariantProcessor, self).__init__(**kwargs)

    def process_data(self, data: Any) -> Any:
        if self.parser:
            data = self.parser.parse(data)

        if self.query:
            data = self.query.parse(data)

        variants_data: Dict[Optional[str], Any] = {}

        for data_info in data:
            variant_key = self._get_variant_key(data_info)

            if self.with_variant_values and self.variant_values_lower:
                if variant_key:
                    variant_key = variant_key.lower()

            if variant_key not in variants_data:
                variants_data[variant_key] = []

            variants_data[variant_key].append(data_info)

        if not self.multi_values:
            variants_data = {k: v[0] for k, v in variants_data.items() if v}

        if self.with_variant_values:
            return variants_data

        return list(variants_data.values())

    def _get_variant_key(self, data: Any) -> Optional[str]:
        if self.variant_parser:
            return self.variant_parser.parse(data)
        elif self.variant_query:
            return self.variant_query.parse(data)

        return None
