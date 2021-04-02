from abc import ABC
from typing import Any, List, Optional, Union

from easytxt import parse_text

from easydata.parsers.base import BaseData

__all__ = (
    "Description",
    "Sentences",
    "Features",
    "FeaturesDict",
    "Feature",
)


class BaseDescription(BaseData, ABC):
    def __init__(
        self,
        *args,
        language: Optional[str] = None,
        allow: Optional[Union[str, List[str]]] = None,
        callow: Optional[Union[str, List[str]]] = None,
        from_allow: Optional[Union[str, List[str]]] = None,
        from_callow: Optional[Union[str, List[str]]] = None,
        to_allow: Optional[Union[str, List[str]]] = None,
        to_callow: Optional[Union[str, List[str]]] = None,
        deny: Optional[Union[str, List[str]]] = None,
        cdeny: Optional[Union[str, List[str]]] = None,
        normalize: bool = True,
        capitalize: bool = True,
        title: bool = False,
        uppercase: bool = False,
        lowercase: bool = False,
        min_chars: int = 5,
        replace_keys: Optional[list] = None,
        remove_keys: Optional[list] = None,
        replace_keys_raw_text: Optional[list] = None,
        remove_keys_raw_text: Optional[list] = None,
        split_inline_breaks: bool = True,
        inline_breaks: Optional[List[str]] = None,
        merge_sentences: bool = True,
        stop_key: str = ".",
        stop_keys_split: Optional[List[str]] = None,
        stop_keys_ignore: Optional[List[str]] = None,
        sentence_separator: str = " ",
        feature_split_keys: Optional[List[str]] = None,
        text_num_to_numeric: bool = False,
        autodetect_html: bool = True,
        **kwargs,
    ):

        self._allow = allow
        self._callow = callow
        self._from_allow = from_allow
        self._from_callow = from_callow
        self._to_allow = to_allow
        self._to_callow = to_callow
        self._deny = deny
        self._cdeny = cdeny
        self._normalize = normalize
        self._capitalize = capitalize
        self._title = title
        self._uppercase = uppercase
        self._lowercase = lowercase
        self._min_chars = min_chars
        self._replace_keys = replace_keys
        self._remove_keys = remove_keys
        self._replace_keys_raw_text = replace_keys_raw_text
        self._remove_keys_raw_text = remove_keys_raw_text
        self._split_inline_breaks = split_inline_breaks
        self._inline_breaks = inline_breaks
        self._merge_sentences = merge_sentences
        self._stop_key = stop_key
        self._stop_keys_split = stop_keys_split
        self._stop_keys_ignore = stop_keys_ignore
        self._sentence_separator = sentence_separator
        self._feature_split_keys = feature_split_keys
        self._text_num_to_numeric = text_num_to_numeric
        self._autodetect_html = autodetect_html

        self.__language = language

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _language(self):
        return self.__language or self.config.get("ED_LANGUAGE", "en")

    def _get_text_parser(self, text=Any):
        return parse_text(
            text=text,
            language=self._language,
            from_allow=self._from_allow,
            from_callow=self._from_callow,
            to_allow=self._to_allow,
            to_callow=self._to_callow,
            deny=self._deny,
            cdeny=self._cdeny,
            normalize=self._normalize,
            capitalize=self._capitalize,
            title=self._title,
            uppercase=self._uppercase,
            lowercase=self._lowercase,
            min_chars=self._min_chars,
            replace_keys=self._replace_keys,
            remove_keys=self._remove_keys,
            replace_keys_raw_text=self._replace_keys_raw_text,
            remove_keys_raw_text=self._remove_keys_raw_text,
            split_inline_breaks=self._split_inline_breaks,
            inline_breaks=self._inline_breaks,
            merge_sentences=self._merge_sentences,
            stop_key=self._stop_key,
            stop_keys_split=self._stop_keys_split,
            stop_keys_ignore=self._stop_keys_ignore,
            sentence_separator=self._sentence_separator,
            feature_split_keys=self._feature_split_keys,
            text_num_to_numeric=self._text_num_to_numeric,
            autodetect_html=self._autodetect_html,
        )


class Description(BaseDescription):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ) -> Optional[str]:

        return self._get_text_parser(value).text or None


class Sentences(BaseDescription):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ) -> Optional[list]:

        return self._get_text_parser(value).sentences


class Features(BaseDescription):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ) -> Optional[list]:

        return self._get_text_parser(value).features


class FeaturesDict(BaseDescription):
    def _parse_value(
        self,
        value: Any,
        data: Any,
    ) -> Optional[list]:

        return self._get_text_parser(value).features_dict


class Feature(BaseDescription):
    def __init__(
        self,
        *args,
        key: Optional[str] = None,
        key_exact: Optional[str] = None,
        **kwargs,
    ):

        if not key and not key_exact:
            raise AttributeError("feature attr key or key_exact must be provided!")

        self._key = key
        self._key_exact = key_exact

        super().__init__(
            *args,
            **kwargs,
        )

    def _parse_value(self, value: Any, data: Any) -> Optional[list]:

        text_parser = self._get_text_parser(value)

        if self._key_exact:
            return text_parser.feature_exact(self._key_exact)

        return text_parser.feature(self._key)
