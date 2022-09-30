import pytest

import easydata as ed

test_date_sentence = "It has happened on 10 Dec 2018 at 10:55:50."


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.DateTime(), "Fri, 10 Dec 2018 10:55:50", "12/10/2018 10:55:50"),
        # DateTime shouldn't extract date from sentence
        (ed.DateTime(), test_date_sentence, None),
        (ed.Date(), "Fri, 10 Dec 2018 10:55:50", "12/10/2018"),
        (ed.Date(), "17 Sep 2022", "09/17/2022"),
        (ed.Date(), "Sep 17 2022", "09/17/2022"),
        (ed.Date(), "Sep. 17 2022", "09/17/2022"),
        (ed.Date(prefer_dates_from="future"), "jan 4", "01/04/2023"),
        (ed.YearSearch(), test_date_sentence, "2018"),
        (ed.YearSearch(), "Some player signed 2010 Open 139th (British Open)", "2010"),
        (ed.TimeSearch(), test_date_sentence, "10:55:50"),
        (ed.DateSearch(), test_date_sentence, "12/10/2018"),
        (ed.DateSearch(), "dec 11", "12/11/2022"),
        (ed.DateSearch(), "jan 4", "01/04/2022"),
        (ed.DateSearch(prefer_dates_from="future"), "jan 4", "01/04/2023"),
        (
            ed.DateSearch(prefer_dates_from="future", remove_keys=[r"\."]),
            "jan. 4",
            "01/04/2023",
        ),
        (ed.DateTimeSearch(), test_date_sentence, "12/10/2018 10:55:50"),
        (ed.Year(), "Fri, 10 Dec 2018 10:55:50", "2018"),
        (ed.Year(max_year=2017), "Fri, 10 Dec 2018 10:55:50", None),
        (ed.Year(max_year=2020), "Fri, 10 Dec 2018 10:55:50", "2018"),
        (ed.Year(max_year=2018), "Fri, 10 Dec 2018 10:55:50", "2018"),
        (ed.Year(min_year=2019), "Fri, 10 Dec 2018 10:55:50", None),
        (ed.Year(min_year=2016), "Fri, 10 Dec 2018 10:55:50", "2018"),
        (ed.Year(min_year=2018), "Fri, 10 Dec 2018 10:55:50", "2018"),
        (ed.Time(), "Fri, 10 Dec 2018 10:55:50", "10:55:50"),
        (ed.Time(time_format="%H-%M-%S"), "Fri, 10 Dec 2018 10:55:50", "10-55-50"),
        (
            ed.Time().init_config({"ED_TIME_FORMAT": "%H-%M-%S"}),
            "Fri, 10 Dec 2018 10:55:50",
            "10-55-50",
        ),
        (
            ed.DateTime(datetime_format="%d.%m.%Y %H:%M:%S"),
            "Fri, 10 Dec 2018 10:55:50",
            "10.12.2018 10:55:50",
        ),
        (
            ed.DateTime().init_config({"ED_DATETIME_FORMAT": "%d.%m.%Y %H:%M:%S"}),
            "Fri, 10 Dec 2018 10:55:50",
            "10.12.2018 10:55:50",
        ),
        (ed.Date(date_format="%d.%m.%Y"), "Fri, 10 Dec 2018 10:55:50", "10.12.2018"),
        (
            ed.Date().init_config({"ED_DATE_FORMAT": "%d.%m.%Y"}),
            "Fri, 10 Dec 2018 10:55:50",
            "10.12.2018",
        ),
        (ed.SPDateTime(), "2018-12-10T10:55:50", "12/10/2018 10:55:50"),
        (
            ed.SPDateTime(sp_datetime_format="%Y/%m/%d %H:%M:%S"),
            "2018/12/10 10:55:50",
            "12/10/2018 10:55:50",
        ),
        (
            ed.SPDateTime(
                sp_datetime_format="%Y/%m/%d %H:%M:%S",
                datetime_format="%m-%d-%YT%H:%M:%S",
            ),
            "2018/12/10 10:55:50",
            "12-10-2018T10:55:50",
        ),
        (ed.SPDate(), "2018-12-10", "12/10/2018"),
        (ed.SPDate(sp_date_format="%Y/%m/%d"), "2018/12/10", "12/10/2018"),
        (ed.SPDate(date_format="%m-%d-%Y"), "2018-12-10", "12-10-2018"),
    ],
)
def test_year_search(parser, test_data, result):
    assert parser.parse(test_data) == result
