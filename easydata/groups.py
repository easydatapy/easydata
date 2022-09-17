from typing import Any, List, Optional

from easydata.parsers.base import Base
from easydata.queries.base import QuerySearchBase
from easydata.utils import mix, parse

__all__ = ("ItemGroup",)


class ItemGroup(Base):
    query: Optional[QuerySearchBase] = None

    source: str = "main"

    def __init__(self):
        self._group_item_parsers = {}
        self._group_item_protected_names = []

        self._load_item_parsers_from_group()

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        if self.source or self.query:
            parent_data = data
            with_parent_data = True

        data = self._process_data(data, parent_data)

        item_data = {}

        for name, parser in self._group_item_parsers.items():
            if with_parent_data:
                value = mix.process_item_parser(parser, parent_data, data, True)
            else:
                value = mix.process_item_parser(parser, data)

            item_data[name] = value

        return item_data

    def _process_data(
        self,
        data: Any,
        parent_data: Any = None,
    ) -> Any:

        if self.source:
            data = data[self.source]

        if self.query:
            data = parse.query_parser(
                query=self.query,
                data=data,
                source=self.source,
                parent_data=parent_data,
            )

        return data

    def _load_item_parsers_from_group(self):
        item_attr_items = mix.iter_attr_data_from_obj(
            obj=self,
            attr_prefixes=["item_", "_item_"],
        )

        for item_name, parser_method in item_attr_items:
            if item_name.startswith("item_"):
                item_name = item_name.replace("item_", "")

            if item_name.startswith("_item_"):
                item_name = item_name.replace("_item_", "")

                if item_name not in self._group_item_protected_names:
                    self._group_item_protected_names.append(item_name)

            self._group_item_parsers[item_name] = parser_method

    @property
    def group_item_protected_names(self) -> List[str]:
        return self._group_item_protected_names
