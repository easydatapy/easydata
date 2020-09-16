from typing import Any, Optional

from easydata.parsers.text import Text
from easydata.utils import email

__all__ = ("Email",)


class Email(Text):
    def __init__(
        self,
        *args,
        domain: Optional[str] = None,
        **kwargs,
    ):

        self._domain = domain

        super().__init__(
            *args,
            **kwargs,
        )

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super()._parse_value(value=value, data=data)

        if not value:
            return None

        if self._domain:
            email_value = email.search_one(value)

            # no need for adding a domain since it's already valid email
            if email_value:
                return email_value

            at_symbol = "" if value.endswith("@") else "@"

            value = "{}{}{}".format(value, at_symbol, self._domain)

        return email.search_one(value)
