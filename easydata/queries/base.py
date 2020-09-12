from abc import ABC, abstractmethod
from typing import Any, Optional

from easydata.utils import validate


class QuerySearch(ABC):
    def get(
        self,
        data: Any,
        source: str = "data",
    ) -> Any:

        validate.if_data_bag_with_source(
            data=data,
            source=source,
        )

        if not data:
            return None

        data = self._process_data(data, source)

        return self._parse(data)

    @abstractmethod
    def _parse(
        self,
        data: Any,
    ):
        pass

    @abstractmethod
    def _process_data(
        self,
        data: Any,
        source: Optional[str] = None,
    ) -> Any:
        pass
