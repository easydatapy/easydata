import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import xmltodict
import yaml
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

        self._source = source
        self._new_source = new_source
        self._process_source_data = process_source_data

    def parse(self, data: DataBag) -> DataBag:
        new_source = self._new_source

        source_data = data[self._source]

        if self._process_source_data:
            source_data = self._process_source_data(source_data)

        trans_data = self._process_data(source_data)

        if new_source is None:
            original_source = "{}_raw".format(self._source)
            data[original_source] = data[self._source]

            new_source = self._source

        data[new_source] = trans_data

        return data

    def parse_data(self, data=None, **kwargs):
        if data:
            kwargs["data"] = data

        data = DataBag(self, **kwargs)

        return self.parse(data)

    @abstractmethod
    def _process_data(self, source_data) -> Any:
        pass


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
        query: Union[List[QuerySearch], QuerySearch],
        **kwargs,
    ):

        if isinstance(query, QuerySearch):
            self._query = [query]

        super().__init__(**kwargs)

    def _process_data(self, data: Any) -> Any:
        return parse.query_search(self._query, data)


class DataJsonFromQueryToDictProcessor(DataFromQueryProcessor):
    def process_data(self, data: Any) -> Any:
        jt = super()._process_data(data)

        return json.loads(jt)


class DataTextFromReProcessor(DataBaseProcessor):
    def __init__(
        self,
        *args,
        re_query,
        multi=False,
        dotall=True,
        none_if_empty=False,
        process_value=None,
        **kwargs,
    ):

        self._re_query = re_query
        self._multi = multi
        self._dotall = dotall
        self._none_if_empty = none_if_empty
        self._process_value = process_value

        super().__init__(*args, **kwargs)

    def _process_data(self, source_data: str) -> Any:
        results = re.findall(self._re_query, source_data, re.DOTALL)

        if not results:
            if self._none_if_empty:
                return None

            error_msg = 'No matches were found for a re queries "{}"'
            raise ValueError(error_msg.format(self._re_query))

        if self._process_value:
            results = [self._process_value(result) for result in results]

        return results if self._multi else results[0]


class DataJsonFromReToDictProcessor(DataTextFromReProcessor):
    def _process_data(self, source_data: str) -> Any:
        res = super()._process_data(source_data)

        if not res:
            return None

        if self._multi:
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

        self._parser = parser
        self._variant_parser = variant_parser
        self._query = query
        self._variant_query = variant_query
        self._multi_values = multi_values
        self._with_variant_values = with_variant_values
        self._variant_values_lower = variant_values_lower

        super().__init__(**kwargs)

    def _process_data(self, data: Any) -> Any:
        if self._parser:
            data = self._parser.parse(data)

        if self._query:
            data = self._query.get(data)

        variants_data: Dict[Optional[str], Any] = {}

        for data_info in data:
            variant_key = self._get_variant_key(data_info)

            if self._with_variant_values and self._variant_values_lower:
                if variant_key:
                    variant_key = variant_key.lower()

            if variant_key not in variants_data:
                variants_data[variant_key] = []

            variants_data[variant_key].append(data_info)

        if not self._multi_values:
            variants_data = {k: v[0] for k, v in variants_data.items() if v}

        if self._with_variant_values:
            return variants_data

        return list(variants_data.values())

    def _get_variant_key(self, data: Any) -> Optional[str]:
        if self._variant_parser:
            return self._variant_parser.parse(data)
        elif self._variant_query:
            return self._variant_query.get(data)

        return None
