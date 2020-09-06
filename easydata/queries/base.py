from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional

from easydata.data import DataBag


class QuerySearch(ABC):
    def get(
        self,
        data: Any,
        source: str = "data",
    ) -> Any:

        self.validate_data(data, source)

        if not data:
            return data

        data = self.process_data(data, source)

        return self.parse(data)

    def get_all(
        self,
        data: Any,
        source: str = "data",
    ) -> Any:
        return list(self.get_iter(data, source))

    def get_iter(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Iterable[Any]:

        self.validate_data(data, source)

        if not data:
            return data

        data = self.process_data(data, source)

        yield from self.iter_parse(data)

    def validate_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ):

        if isinstance(data, DataBag) and not source:
            raise AttributeError(
                "data of type DataBag needs also source attribute value"
            )

    @abstractmethod
    def parse(
        self,
        data: Any,
    ):
        pass

    @abstractmethod
    def iter_parse(
        self,
        data: Any,
    ) -> Iterable[Any]:
        pass

    @abstractmethod
    def process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:
        pass
