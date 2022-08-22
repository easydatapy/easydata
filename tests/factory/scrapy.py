from typing import Optional

from scrapy.http import Request, TextResponse


def fake_response(
    url: str,
    body: str,
    meta: Optional[dict] = None,
    encoding: str = "utf-8",
    cb_kwargs: Optional[dict] = None,
):

    request = Request(
        url=url,
        encoding=encoding,
        meta=meta,
        cb_kwargs=cb_kwargs,
    )

    return TextResponse(
        url=url,
        body=body,
        encoding=encoding,
        request=request,
    )
