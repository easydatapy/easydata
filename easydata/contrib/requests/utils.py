from requests import Response

from easydata.data import DataBag


def response_to_data_bag(
    response: Response,
    to_json: bool = False,
    **kwargs,
):

    main = response.json() if to_json else response.text

    data_args = {
        "main": main,
        "url": response.url,
        "headers": response.headers,
    }

    kwargs = {**data_args, **kwargs}

    return DataBag(**kwargs)
