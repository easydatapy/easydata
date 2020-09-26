from functools import lru_cache
from typing import Any, List, Optional

from easytxt import text

from easydata.data import DataBag
from easydata.parsers.base import Base
from easydata.parsers.bool import Bool
from easydata.parsers.text import Text
from easydata.queries.base import QuerySearch
from easydata.utils import mix

__all__ = ("Choice",)


class Choice(Base):
    def __init__(
        self,
        choices: list,
        lookup_queries: Optional[List[QuerySearch]] = None,
        lookup_parsers: Optional[List[Base]] = None,
        lookup_items: Optional[List[str]] = None,
        default_choice: Optional[str] = None,
        source: Optional[str] = None,
    ):

        self._has_lookup = bool(lookup_queries or lookup_parsers or lookup_items)

        self._lookup_queries = lookup_queries
        self._lookup_items = lookup_items
        self._choices = choices
        self._default_choice = default_choice
        self._source = source or "main"

        self.__lookup_parsers = lookup_parsers

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Optional[str]:

        lookup_values = []

        lookup_data = parent_data if with_parent_data else data

        if self._has_lookup:
            if self._lookup_items and isinstance(data, DataBag):
                lookup_values += list(self._get_str_value_from_lookup_items(data))

            lookup_values += list(self._get_str_value_from_lookup_parsers(lookup_data))
        else:
            if isinstance(lookup_data, DataBag):
                lookup_data = lookup_data[self._source]

            lookup_values.append(text.to_str(lookup_data))

        return self._get_choice_value(lookup_values, data) or self._default_choice

    def _get_choice_value(
        self,
        lookup_values: List[str],
        data: Any,
    ) -> Optional[str]:

        lookup_value = " ".join(lookup_values)

        for choice_data in self._choices:
            choice_value, choice_search_data = choice_data

            if isinstance(choice_search_data, Bool):
                choice_search_data.init_config(self.config)

                if choice_search_data.parse(data=data):
                    return choice_value
            elif lookup_value and text.contains(lookup_value, choice_search_data):
                return choice_value

        return None

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def _lookup_parsers(self):
        lookup_parsers = []

        if self._lookup_queries:
            for lookup_query in self._lookup_queries:
                text_parser = Text(
                    query=lookup_query,
                    source=self._source,
                )

                lookup_parsers.append(text_parser)

        if self.__lookup_parsers:
            lookup_parsers += self.__lookup_parsers

        for lookup_parser in lookup_parsers:
            mix.validate_parser(lookup_parser)

            lookup_parser.init_config(self.config)

        return lookup_parsers

    def _get_str_value_from_lookup_items(self, data: Any):
        if self._lookup_items:
            for lookup_item in self._lookup_items:
                lookup_value = data.get(lookup_item)

                if lookup_value:
                    yield text.to_str(lookup_value)

    def _get_str_value_from_lookup_parsers(self, data: Any):
        for lookup_parser in self._lookup_parsers:  # type: ignore
            lookup_value = lookup_parser.parse(data)

            if lookup_value:
                yield text.to_str(lookup_value)
