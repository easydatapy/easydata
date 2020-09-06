import pytest

from easydata import parsers

test_date_text = "Fri, 10 Dec 2018 10:55:50"

test_date_sentence = "It has happened on 10 Dec 2018 at 10:55:50."


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_text, "12/10/2018 10:55:50"),
        # DateTime shouldn't extract date from sentence
        (test_date_sentence, None),
    ],
)
def test_datetime(test_data, result):
    time_parser = parsers.DateTime()
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "datetime_format, test_data, result",
    [
        ("%d.%m.%Y %H:%M:%S", test_date_text, "10.12.2018 10:55:50"),
    ],
)
def test_datetime_custom_datetime_format(datetime_format, test_data, result):
    time_parser = parsers.DateTime(datetime_format=datetime_format)
    assert time_parser.parse(test_data) == result


def test_datetime_config():
    time_parser = parsers.DateTime()
    time_parser.init_config({"ED_DATETIME_FORMAT": "%d.%m.%Y %H:%M:%S"})
    assert time_parser.parse(test_date_text) == "10.12.2018 10:55:50"


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_text, "12/10/2018"),
    ],
)
def test_date(test_data, result):
    time_parser = parsers.Date()
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "date_format, test_data, result",
    [
        ("%d.%m.%Y", test_date_text, "10.12.2018"),
    ],
)
def test_date_custom_date_format(date_format, test_data, result):
    time_parser = parsers.Date(date_format=date_format)
    assert time_parser.parse(test_data) == result


def test_date_config():
    time_parser = parsers.Date()
    time_parser.init_config({"ED_DATE_FORMAT": "%d.%m.%Y"})
    assert time_parser.parse(test_date_text) == "10.12.2018"


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_text, "10:55:50"),
    ],
)
def test_time(test_data, result):
    time_parser = parsers.Time()
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "time_format, test_data, result",
    [
        ("%H-%M-%S", test_date_text, "10-55-50"),
    ],
)
def test_time_custom_time_format(time_format, test_data, result):
    time_parser = parsers.Time(time_format=time_format)
    assert time_parser.parse(test_data) == result


def test_time_config():
    time_parser = parsers.Time()
    time_parser.init_config({"ED_TIME_FORMAT": "%H-%M-%S"})
    assert time_parser.parse(test_date_text) == "10-55-50"


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_text, "2018"),
    ],
)
def test_year(test_data, result):
    time_parser = parsers.Year()
    assert time_parser.parse(test_data) == "2018"


@pytest.mark.parametrize(
    "min_year, test_data, result",
    [
        (2019, test_date_text, None),
        (2016, test_date_text, "2018"),
        (2018, test_date_text, "2018"),
    ],
)
def test_year_min_year(min_year, test_data, result):
    time_parser = parsers.Year(min_year=min_year)
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "max_year, test_data, result",
    [
        (2017, test_date_text, None),
        (2020, test_date_text, "2018"),
        (2018, test_date_text, "2018"),
    ],
)
def test_year_max_year(max_year, test_data, result):
    time_parser = parsers.Year(max_year=max_year)
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_sentence, "12/10/2018 10:55:50"),
    ],
)
def test_datetime_search(test_data, result):
    time_parser = parsers.DateTimeSearch()
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_sentence, "12/10/2018"),
    ],
)
def test_date_search(test_data, result):
    time_parser = parsers.DateSearch()
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_sentence, "10:55:50"),
    ],
)
def test_time_search(test_data, result):
    time_parser = parsers.TimeSearch()
    assert time_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, result",
    [
        (test_date_sentence, "2018"),
        ("Some player signed 2010 Open 139th (British Open)", "2010"),
    ],
)
def test_year_search(test_data, result):
    time_parser = parsers.YearSearch()
    assert time_parser.parse(test_data) == result
