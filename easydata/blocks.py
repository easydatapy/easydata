from copy import copy
from typing import Optional, Type

from easydata.models import ItemModel
from easydata.parsers.base import BaseData
from easydata.parsers.data import Data
from easydata.parsers.number import SearchFloat, SearchInt
from easydata.parsers.price import PriceFloat, PriceInt, PriceText
from easydata.parsers.text import Text
from easydata.queries.base import QuerySearch

__all__ = (
    "BlockParserModel",
    "BlockSimpleDataModel",
    "BlockSimpleTextModel",
    "BlockSimpleSearchFloatModel",
    "BlockSimpleSearchIntModel",
    "BlockSimplePriceFloatModel",
    "BlockSimplePriceIntModel",
    "BlockSimplePriceTextModel",
)


class BlockParserModel(ItemModel):
    def __init__(
        self,
        parser: BaseData,
        source: Optional[str] = None,
        query_prefix: Optional[str] = None,
        **queries,
    ):

        for name, query in queries.items():
            item_parser = copy(parser)

            if query_prefix and isinstance(query, QuerySearch):
                query.add_query_prefix(query_prefix)

            if source:
                item_parser.add_source(source)

            item_parser.add_query(query)

            setattr(
                self,
                "item_{}".format(name),
                item_parser,
            )


class BlockSimpleBaseModel(ItemModel):
    default_parser_cls: Optional[Type[BaseData]] = None

    def __init__(
        self,
        source: Optional[str] = None,
        query_prefix: Optional[str] = None,
        **queries,
    ):

        for name, query in queries.items():
            if query_prefix and isinstance(query, QuerySearch):
                query.add_query_prefix(query_prefix)

            if self.default_parser_cls is None:
                raise NotImplementedError(
                    "Parser cls in a default_parser_cls property must be implemented",
                )

            setattr(
                self,
                "item_{}".format(name),
                self.default_parser_cls(
                    query=query,
                    source=source,
                ),
            )


class BlockSimpleDataModel(BlockSimpleBaseModel):
    default_parser_cls = Data


class BlockSimpleTextModel(BlockSimpleBaseModel):
    default_parser_cls = Text


class BlockSimpleSearchFloatModel(BlockSimpleBaseModel):
    default_parser_cls = SearchFloat


class BlockSimpleSearchIntModel(BlockSimpleBaseModel):
    default_parser_cls = SearchInt


class BlockSimplePriceFloatModel(BlockSimpleBaseModel):
    default_parser_cls = PriceFloat


class BlockSimplePriceIntModel(BlockSimpleBaseModel):
    default_parser_cls = PriceInt


class BlockSimplePriceTextModel(BlockSimpleBaseModel):
    default_parser_cls = PriceText
