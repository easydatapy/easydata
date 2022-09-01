from typing import Callable
from typing import Union as UnionType

from easydata.parsers.base import Base, BaseData
from easydata.queries.base import QuerySearchBase

Parser = UnionType[Base, BaseData, Callable]

QueryDataParser = UnionType[QuerySearchBase, BaseData]
