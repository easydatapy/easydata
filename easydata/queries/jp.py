from typing import Any, Optional

import jmespath

from easydata.queries.key import KeyQuery


class JMESPathSearch(KeyQuery):
    def _parse(
        self,
        data: Any,
        query: Optional[str],
    ):

        if query:
            data = jmespath.search(
                expression=query,
                data=data,
            )

        return self._process_data_key_values(data)
