from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional

from easydata.data import DataBag


class QuerySearch(ABC):
    def get(
        self,
        data: Any,
        source: str = "data",
    ) -> Any:

        self._validate_data(data, source)

        if not data:
            return data

        data = self._process_data(data, source)

        return self._parse(data)

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

        self._validate_data(data, source)

        if not data:
            return data

        data = self._process_data(data, source)

        yield from self._iter_parse(data)

    def _validate_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ):

        if isinstance(data, DataBag) and not source:
            raise AttributeError(
                "data of type DataBag needs also source attribute value"
            )

    @abstractmethod
    def _parse(
        self,
        data: Any,
    ):
        pass

    @abstractmethod
    def _iter_parse(
        self,
        data: Any,
    ) -> Iterable[Any]:
        pass

    @abstractmethod
    def _process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:
        pass
