from typing import Any

import jmespath

from easydata.queries.key import KeyQuery


class JMESPathSearch(KeyQuery):
    def _parse(
        self,
        data: Any,
    ):

        if self._query:
            data = jmespath.search(
                expression=self._query,
                data=data,
            )

        return self._process_data_key_values(data)
