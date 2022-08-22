from typing import List, Optional

from scrapy.http.response import Response

from easydata.data import DataBag


def response_to_data_bag(
    response: Response,
    meta_to_data_values: Optional[List[str]] = None,
    meta_to_data_enable: bool = True,
    **kwargs,
):

    data_args = {
        "main": response.body,
        "url": response.url,
        "headers": response.headers,
    }

    if meta_to_data_enable and response.meta:
        for meta_key, meta_data in response.meta.items():
            if meta_to_data_values and meta_key not in meta_to_data_values:
                continue

            data_args[meta_key] = meta_data

    kwargs = {**data_args, **kwargs}

    return DataBag(**kwargs)
