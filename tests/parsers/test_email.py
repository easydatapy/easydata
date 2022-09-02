import pytest

import easydata as ed

default_email = "easydatapy@gmail.com"


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.Email(), "easydatapy@gmail.com", default_email),
        (ed.Email(), "contact:easydatapy@gmail.com'", default_email),
        (ed.Email(), "contact;easydatapy@gmail.com", default_email),
        (ed.Email(), '<input value="easydatapy@gmail.com">', default_email),
        (ed.Email(), '<a href="mailto:easydatapy@gmail.com">Here</a>', default_email),
        (ed.Email(), "Contact please easydatapy@gmail.com!!!", default_email),
        (ed.Email(), ",easydatapy@gmail.com,", default_email),
        (ed.Email(), "Contact please EasyDataPY@gmail.com!!!", "EasyDataPY@gmail.com"),
        (ed.Email(), "easy.datapy@gmail.com", "easy.datapy@gmail.com"),
        (
            ed.Email(),
            "1ea-12sy.da_ta4.py99@gmail.com",
            "1ea-12sy.da_ta4.py99@gmail.com",
        ),
        (ed.Email(), "easydatapy@gmail.co.uk", "easydatapy@gmail.co.uk"),
        (ed.Email(), "easydatapy@hotmail.info", "easydatapy@hotmail.info"),
        (ed.Email(), "easydatapy@hotmail.si", "easydatapy@hotmail.si"),
        (ed.Email(), "easydatapy@gmail.COM", "easydatapy@gmail.COM"),
        (ed.Email(), "EASYdatapy@GMAIL.COM", "EASYdatapy@GMAIL.COM"),
        (ed.Email(), "Uppercase works to EASYdatapy@GMAIL.COM", "EASYdatapy@GMAIL.COM"),
        (ed.Email(), "easydatapy@gmail", None),
        (ed.Email(), "easydatapy@", None),
        (ed.Email(), "@gmail.com", None),
        (ed.Email(), None, None),
        (ed.Email(), "", None),
        (ed.Email(domain="gmail.com"), "easydatapy", default_email),
        (ed.Email(domain="gmail.com"), "easydatapy@", default_email),
        (ed.Email(domain="gmail.com"), "Contact please easydatapy@", default_email),
        (ed.Email(domain="gmail.com"), "Contact please easydatapy@ !!!", None),
        (ed.Email(domain="gmail.com"), "easydatapy@@", None),
        (ed.Email(domain="gmail"), "easydatapy@", None),
        (ed.Email(lowercase=True), "EASYdatapy@GMAIL.COM", "easydatapy@gmail.com"),
    ],
)
def test_email(parser, test_data, result):
    assert parser.parse(test_data) == result
