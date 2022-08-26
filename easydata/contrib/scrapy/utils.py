from typing import List, Optional, Union

from scrapy.http.response import Response
from scrapy.http.response.text import TextResponse

from easydata.data import DataBag


def response_to_data_bag(
    response: Union[Response, TextResponse],
    to_json: bool = False,
    meta_to_data_values: Optional[List[str]] = None,
    meta_to_data_enable: bool = True,
    **kwargs,
):

    if to_json:
        if not hasattr(response, "json"):
            raise AttributeError("Response instance must support json method!")

        main_data = response.json()
    else:
        main_data = response.text

    data_args = {
        "main": main_data,
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
