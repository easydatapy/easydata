from typing import Any, Optional, Union

from easydata.parsers.text import Text
from easydata.utils import url

__all__ = ("Url",)


class Url(Text):
    def __init__(
        self,
        *args,
        from_text: bool = False,
        from_qs: Optional[str] = None,
        from_qs_unquote: Optional[str] = None,
        remove_qs: Optional[Union[str, list, bool]] = None,
        qs: Optional[dict] = None,
        domain: Optional[str] = None,
        protocol: Optional[str] = None,
        normalize: bool = True,
        **kwargs,
    ):

        self._from_text = from_text
        self._from_qs = from_qs
        self._from_qs_unquote = from_qs_unquote
        self._remove_qs = remove_qs
        self._qs = qs
        self._normalize_url = normalize

        self.__domain = domain
        self.__protocol = protocol

        super().__init__(
            *args,
            normalize=False,
            **kwargs,
        )

    @property
    def _domain(self):
        return self.__domain or self.config["ED_URL_DOMAIN"]

    @property
    def _protocol(self):
        return self.__protocol or self.config["ED_URL_PROTOCOL"]

    def _parse_value(
        self,
        value: Any,
        data: Any,
    ) -> str:

        value = super()._parse_value(value, data)

        if value and self._from_text:
            value = url.from_text(value)

        if value and (self._domain or self._normalize_url):
            value = url.normalize(
                url=value,
                domain=self._domain,
                protocol=self._protocol,
            )

        if self._from_qs:
            value = url.get_value_from_qs(value, self._from_qs)

        if value and self._remove_qs is not None:
            if isinstance(self._remove_qs, bool):
                if self._remove_qs is False:
                    raise ValueError(
                        "remove_qs only accepts True if bool type is provided!"
                    )

                value = url.remove_qs(value)
            else:
                value = url.remove_qs(value, self._remove_qs)

        if value and self._qs:
            value = url.set_qs_values(value, self._qs)

        return value
