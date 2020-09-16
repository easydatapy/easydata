import pytest

from easydata import parsers

default_email = "easydatapy@gmail.com"


@pytest.mark.parametrize(
    "test_data, result",
    [
        ("easydatapy@gmail.com", default_email),
        ("contact:easydatapy@gmail.com'", default_email),
        ("contact;easydatapy@gmail.com", default_email),
        ('<input value="easydatapy@gmail.com">', default_email),
        ('<a href="mailto:easydatapy@gmail.com">Here</a>', default_email),
        ("Contact please easydatapy@gmail.com!!!", default_email),
        (",easydatapy@gmail.com,", default_email),
        ("Contact please EasyDataPY@gmail.com!!!", "EasyDataPY@gmail.com"),
        ("easy.datapy@gmail.com", "easy.datapy@gmail.com"),
        ("1ea-12sy.da_ta4.py99@gmail.com", "1ea-12sy.da_ta4.py99@gmail.com"),
        ("easydatapy@gmail.co.uk", "easydatapy@gmail.co.uk"),
        ("easydatapy@hotmail.info", "easydatapy@hotmail.info"),
        ("easydatapy@hotmail.si", "easydatapy@hotmail.si"),
        ("easydatapy@gmail.COM", "easydatapy@gmail.COM"),
        ("EASYdatapy@GMAIL.COM", "EASYdatapy@GMAIL.COM"),
        ("Uppercase works to EASYdatapy@GMAIL.COM", "EASYdatapy@GMAIL.COM"),
        ("easydatapy@gmail", None),
        ("easydatapy@", None),
        ("@gmail.com", None),
        (None, None),
        ("", None),
    ],
)
def test_email(test_data, result):
    price_parser = parsers.Email()
    assert price_parser.parse(test_data) == result


@pytest.mark.parametrize(
    "test_data, domain, result",
    [
        ("easydatapy", "gmail.com", default_email),
        ("easydatapy@", "gmail.com", default_email),
        ("Contact please easydatapy@", "gmail.com", default_email),
        ("Contact please easydatapy@ !!!", "gmail.com", None),
        ("easydatapy@@", "gmail.com", None),
        ("easydatapy@", "gmail", None),
    ],
)
def test_email_domain(test_data, domain, result):
    price_parser = parsers.Email(domain=domain)
    assert price_parser.parse(test_data) == result


def test_email_domain_lowercase():
    test_data = "EASYdatapy@GMAIL.COM"
    assert parsers.Email(lowercase=True).parse(test_data) == "easydatapy@gmail.com"
