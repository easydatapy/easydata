from typing import Callable
from typing import Union as UnionType

from easydata.parsers.base import Base, BaseData

Parser = UnionType[Base, BaseData, Callable]
