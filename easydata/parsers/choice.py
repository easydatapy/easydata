from abc import ABC
from functools import lru_cache
from typing import Any, List, Optional

from easytxt import text

from easydata.data import DataBag
from easydata.parsers.base import Base
from easydata.parsers.bool import Bool
from easydata.parsers.text import Text
from easydata.queries.base import QuerySearch
from easydata.utils import mix

__all__ = (
    "BaseLookups",
    "Choice",
)


class BaseLookups(Base, ABC):
    def __init__(
        self,
        lookups: Optional[Any] = None,
        source: Optional[str] = None,
    ):

        self._lookups = lookups
        self._source = source or "main"

    def _parse_lookups(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ):

        lookup_data = parent_data if with_parent_data else data

        if not self._lookups:
            if isinstance(lookup_data, DataBag):
                lookup_data = lookup_data[self._source]

            return [text.to_str(lookup_data)]

        lookup_values = []

        for lookup in self._initialized_lookups:
            if isinstance(lookup, str):
                lookup_value = data.get(lookup)
            else:
                lookup_value = lookup.parse(data)

            if lookup_value:
                lookup_values.append(text.to_str(lookup_value))

        return lookup_values

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def _initialized_lookups(self):
        initialized_lookups = []

        if not isinstance(self._lookups, (list, tuple)):
            lookups = [self._lookups]
        else:
            lookups = self._lookups

        for lookup in lookups:
            if isinstance(lookup, QuerySearch):
                lookup = Text(query=lookup, source=self._source)

            if isinstance(lookup, Base):
                mix.validate_parser(lookup)

                lookup.init_config(self.config)

            initialized_lookups.append(lookup)

        return initialized_lookups


class Choice(BaseLookups):
    def __init__(self, choices: list, default_choice: Optional[str] = None, **kwargs):

        self._choices = choices
        self._default_choice = default_choice

        super().__init__(**kwargs)

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Optional[str]:

        lookup_values = self._parse_lookups(
            data=data,
            parent_data=parent_data,
            with_parent_data=with_parent_data,
        )

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
