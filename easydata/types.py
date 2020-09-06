from typing import List, Optional, Union

from easydata.queries.base import QuerySearch

RequiredQuerySearch = Union[QuerySearch, List[QuerySearch]]

OptionalQuerySearch = Optional[RequiredQuerySearch]
