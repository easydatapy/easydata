from abc import abstractmethod
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Optional

from dateparser import parse as parse_date
from dateparser.search import search_dates

from easydata.parsers.text import Text

__all__ = (
    "DateTime",
    "Date",
    "Year",
    "Time",
    "DateTimeSearch",
    "DateSearch",
    "TimeSearch",
    "YearSearch",
    "SPDateTime",
    "SPDate",
)


class BaseDateTime(Text):
    def __init__(
        self,
        *args,
        datetime_format: Optional[str] = None,
        min_year: Optional[int] = None,
        max_year: Optional[int] = None,
        today: bool = False,
        **kwargs,
    ):

        self._min_year = min_year
        self._max_year = max_year
        self._today = today

        self.__datetime_format = datetime_format

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _datetime_format(self):
        return self.__datetime_format or self.config["ED_DATETIME_FORMAT"]

    def parse(
        self,
        data: Any,
        parent_data: Any = None,
        with_parent_data: bool = False,
    ) -> Any:

        if self._today:
            datetime_obj = datetime.today()

            return self._parse_datetime_obj_to_str(datetime_obj)

        return super().parse(data, parent_data, with_parent_data)

    def parse_value(
        self,
        value: Any,
        data: Any,
    ):

        value = super(BaseDateTime, self).parse_value(value, data)

        if not value:
            return None

        datetime_obj = self._get_datetime_obj_from_value(value)

        if not datetime_obj:
            return None

        datetime_obj = self._process_datetime_obj(datetime_obj)

        if not datetime_obj:
            return None

        return self._parse_datetime_obj_to_str(datetime_obj)

    @abstractmethod
    def _get_datetime_obj_from_value(self, value: str) -> Optional[datetime]:
        pass

    def _process_datetime_obj(self, datetime_obj: datetime):
        if self._min_year and datetime_obj.year < self._min_year:
            return None

        if self._max_year and datetime_obj.year > self._max_year:
            return None

        return datetime_obj

    def _parse_datetime_obj_to_str(self, datetime_obj: datetime) -> str:
        return datetime_obj.strftime(self._datetime_format)


date_mixin = BaseDateTime if TYPE_CHECKING else object


class DateTime(BaseDateTime):
    search = False

    def __init__(
        self,
        *args,
        language: Optional[str] = None,
        locales: Optional[List[str]] = None,
        region: Optional[str] = None,
        date_formats: Optional[List[str]] = None,
        date_order: Optional[str] = None,
        timezone: Optional[str] = None,
        to_timezone: Optional[str] = None,
        return_as_timezone_aware: Optional[str] = None,
        prefer_day_of_month: Optional[str] = None,
        prefer_dates_from: Optional[str] = None,
        relative_base: Optional[datetime] = None,
        strict_parsing: Optional[bool] = None,
        require_parts: Optional[List[str]] = None,
        skip_tokens: Optional[List[str]] = None,
        date_normalize: Optional[bool] = None,
        return_time_as_period: Optional[bool] = None,
        parsers: Optional[List[str]] = None,
        fuzzy: Optional[bool] = None,
        prefer_locale_date_order: Optional[bool] = None,
        default_languages: Optional[List[str]] = None,
        language_detection_confidence_threshold: Optional[float] = None,
        **kwargs,
    ):

        self.__locales = locales
        self.__region = region
        self.__date_formats = date_formats
        self._date_order = date_order
        self._timezone = timezone
        self._to_timezone = to_timezone
        self._return_as_timezone_aware = return_as_timezone_aware
        self._prefer_day_of_month = prefer_day_of_month
        self._prefer_dates_from = prefer_dates_from
        self._relative_base = relative_base
        self._strict_parsing = strict_parsing
        self._require_parts = require_parts
        self._skip_tokens = skip_tokens
        self._date_normalize = date_normalize
        self._return_time_as_period = return_time_as_period
        self._parsers = parsers
        self._fuzzy = fuzzy
        self._prefer_locale_date_order = prefer_locale_date_order
        self._default_languages = default_languages
        self._language_detection_confidence_threshold = (
            language_detection_confidence_threshold
        )

        super().__init__(
            *args,
            **kwargs,
        )

        self.__language = language

    @cached_property
    def _settings(self) -> Optional[dict]:
        settings = {}

        if self._date_order is not None:
            settings["DATE_ORDER"] = self._date_order

        if self._timezone is not None:
            settings["TIMEZONE"] = self._timezone

        if self._to_timezone is not None:
            settings["TO_TIMEZONE"] = self._to_timezone

        if self._return_as_timezone_aware is not None:
            settings["RETURN_AS_TIMEZONE_AWARE"] = self._return_as_timezone_aware

        if self._prefer_day_of_month is not None:
            settings["PREFER_DAY_OF_MONTH"] = self._prefer_day_of_month

        if self._prefer_dates_from is not None:
            settings["PREFER_DATES_FROM"] = self._prefer_dates_from

        if self._relative_base is not None:
            settings["RELATIVE_BASE"] = self._relative_base  # type: ignore

        if self._strict_parsing is not None:
            settings["STRICT_PARSING"] = self._strict_parsing  # type: ignore

        if self._require_parts is not None:
            settings["REQUIRE_PARTS"] = self._require_parts  # type: ignore

        if self._skip_tokens is not None:
            settings["SKIP_TOKENS"] = self._skip_tokens  # type: ignore

        if self._date_normalize is not None:
            settings["NORMALIZE"] = self._date_normalize  # type: ignore

        if self._return_time_as_period is not None:
            settings["RETURN_TIME_AS_PERIOD"] = (
                self._return_time_as_period  # type: ignore
            )

        if self._parsers is not None:
            settings["PARSERS"] = self._parsers  # type: ignore

        if self._fuzzy is not None:
            settings["FUZZY"] = self._fuzzy  # type: ignore

        if self._prefer_locale_date_order is not None:
            settings["PREFER_LOCALE_DATE_ORDER"] = (
                self._prefer_locale_date_order  # type: ignore
            )

        if self._default_languages is not None:
            settings["DEFAULT_LANGUAGES"] = self._default_languages  # type: ignore

        if self._language_detection_confidence_threshold is not None:
            settings[
                "LANGUAGE_DETECTION_CONFIDENCE_THRESHOLD"
            ] = self._language_detection_confidence_threshold  # type: ignore

        return settings or None

    @property
    def _languages(self):
        if self.__language:
            return [self.__language]

        if self.config["ED_DATETIME_LANGUAGE"]:
            return [self.config["ED_DATETIME_LANGUAGE"]]

        return [self.config["ED_LANGUAGE"]]

    @property
    def _locales(self):
        return self.__locales or self.config["ED_DATETIME_LOCALES"]

    @property
    def _region(self):
        return self.__region or self.config["ED_DATETIME_REGION"]

    @property
    def _date_formats(self):
        return self.__date_formats or self.config["ED_DATETIME_FORMATS"]

    def _get_datetime_obj_from_value(self, value: str) -> Optional[datetime]:
        if self.search:
            matches = search_dates(
                text=value,
                languages=self._languages,
                settings=self._settings,
            )

            return matches[0][-1] if matches else None

        return parse_date(
            date_string=value,
            date_formats=self._date_formats,
            languages=self._languages,
            locales=self._locales,
            region=self._region,
            settings=self._settings,  # type: ignore
        )


class Date(DateTime):
    def __init__(
        self,
        *args,
        date_format: Optional[str] = None,
        **kwargs,
    ):

        self.__date_format = date_format

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _date_format(self):
        return self.__date_format or self.config["ED_DATE_FORMAT"]

    def _parse_datetime_obj_to_str(self, datetime_obj: datetime) -> str:
        return datetime_obj.strftime(self._date_format)


class Time(DateTime):
    def __init__(
        self,
        *args,
        time_format: Optional[str] = None,
        **kwargs,
    ):

        self.__time_format = time_format

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _time_format(self):
        return self.__time_format or self.config["ED_TIME_FORMAT"]

    def _parse_datetime_obj_to_str(self, datetime_obj: datetime) -> str:
        return datetime_obj.strftime(self._time_format)


class Year(DateTime):
    def _parse_datetime_obj_to_str(self, datetime_obj: datetime) -> str:
        return str(datetime_obj.year)


class DateTimeSearch(DateTime):
    search = True


class DateSearch(Date):
    search = True


class YearSearch(Year):
    search = True


class TimeSearch(Time):
    search = True


class SPDateTime(BaseDateTime):
    def __init__(
        self,
        *args,
        sp_datetime_format: Optional[str] = None,
        **kwargs,
    ):

        self.__sp_datetime_format = sp_datetime_format

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _sp_datetime_format(self):
        return self.__sp_datetime_format or self.config["ED_SP_DATETIME_FORMAT"]

    def _get_datetime_obj_from_value(self, value: str) -> Optional[datetime]:
        return datetime.strptime(value, self._sp_datetime_format)


class SPDate(SPDateTime):
    def __init__(
        self,
        *args,
        date_format: Optional[str] = None,
        sp_date_format: Optional[str] = None,
        **kwargs,
    ):

        self.__date_format = date_format
        self.__sp_date_format = sp_date_format

        super().__init__(
            *args,
            **kwargs,
        )

    @property
    def _date_format(self):
        return self.__date_format or self.config["ED_DATE_FORMAT"]

    def _parse_datetime_obj_to_str(self, datetime_obj: datetime) -> str:
        return datetime_obj.strftime(self._date_format)

    @property
    def _sp_date_format(self):
        return self.__sp_date_format or self.config["ED_SP_DATE_FORMAT"]

    def _get_datetime_obj_from_value(self, value: str) -> Optional[datetime]:
        return datetime.strptime(value, self._sp_date_format)
