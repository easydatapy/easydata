import re
from typing import Any, List, Optional, Union
from urllib.parse import parse_qs, urljoin, urlparse

from furl import furl


def get_value_from_qs(
    url: str,
    query_param: str,
):

    parsed = urlparse(url)
    return parse_qs(parsed.query)[query_param][0]


def remove_qs(
    url: str,
    key: Optional[Union[str, list]] = None,
) -> str:

    if key:
        if isinstance(key, str):
            key = [key]

        f = furl(url)

        f.remove(key)

        return f.url

    return url.split("?")[0]


def set_qs_values(
    url: str,
    key_values: dict,
) -> str:

    f = furl(url)

    for key, value in key_values.items():
        f.args[key] = value

    return f.url


def set_qs_value(
    url: str,
    key: str,
    value: Any,
) -> str:

    return set_qs_values(url, {key: value})


def get_path(
    url: str,
    index: Optional[int] = None,
):

    f = furl(url)

    path = f.path

    if index:
        return path.segments[index]

    return str(path)


def normalize(
    url: str,
    domain: Optional[str] = None,
    protocol: str = "https",
):
    protocol = "{}://".format(protocol)

    if domain:
        protocol_domain = urljoin(protocol, domain).replace("///", "//")
    else:
        protocol_domain = protocol

    return urljoin(protocol_domain, url.lstrip(":")).replace("///", "//")


def from_text(text: str) -> Optional[str]:
    results = from_text_multiple(text)
    return results[0] if results else None


def from_text_multiple(text: str) -> Optional[List[str]]:
    re_query = (
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|"
        r"(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )

    return re.findall(re_query, text) or None
