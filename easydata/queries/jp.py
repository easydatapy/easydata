from typing import Any

import jmespath

from easydata.queries.key import KeyQuery


class JmesPathSearch(KeyQuery):
    def _parse(
        self,
        data: Any,
    ):

        data = jmespath.search(
            expression=self._query,
            data=data,
        )

        return self._process_data_key_values(data)
