import pytest
from pyquery import PyQuery

import easydata as ed


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.Text(), "Easybook Pro 13", "Easybook Pro 13"),
        (ed.Text(), "easybook pro 13", "easybook pro 13"),
        (ed.Text(), "Easybook Pro 13 &lt;3 uÌˆnicode", "Easybook Pro 13 <3 ünicode"),
        (ed.Text(), " easybook pro   13", "easybook pro 13"),
        (ed.Text(), " Easybook Pro 13    ", "Easybook Pro 13"),
        (ed.Text(), "Easybook Pro\n13", "Easybook Pro 13"),
        (ed.Text(), None, None),
        (ed.Text(), "", None),
        (ed.Text(), ["Easybook", "pro", 13], "Easybook pro 13"),
        (ed.Text(), ("Easybook", "pro", 13), "Easybook pro 13"),
        (ed.Text(), PyQuery("<div>Easybook Pro 13</div>"), "Easybook Pro 13"),
        (
            ed.Text(normalize=False),
            "Easybook Pro 13 &lt;3 uÌˆnicode",
            "Easybook Pro 13 &lt;3 uÌˆnicode",
        ),
        (
            ed.Text(replace_keys=[("pro", "Air"), ("15", "13")]),
            "Easybook Pro 15",
            "Easybook Air 13",
        ),
        (ed.Text(split_key="-"), "easybook-pro_13", "easybook"),
        (ed.Text(split_key=("-", -1)), "easybook-pro_13", "pro_13"),
        (ed.Text(split_keys=[("-", -1), "_"]), "easybook-pro_13", "pro"),
        (ed.Text(separator="-"), ["Easybook", "pro", 13], "Easybook-pro-13"),
        (ed.Text(separator=" > "), ["Easybook", "pro", 13], "Easybook > pro > 13"),
        (ed.Text(index=0), ["Easybook", "pro", 13], "Easybook"),
        (ed.Text(index=-1), ["Easybook", "pro", 13], "13"),
        (ed.Text(default="Default Value"), None, "Default Value"),
        (ed.Text(default=""), None, ""),
        (ed.Text(take=8), "Easybook Pro 13", "Easybook"),
        (ed.Text(take=30), "Easybook Pro 13", "Easybook Pro 13"),
        (ed.Text(skip=8), "Easybook Pro 13", "Pro 13"),
        (ed.Text(skip=30), "Easybook Pro 13", None),
        (ed.Text(uppercase=True), "Easybook Pro 13", "EASYBOOK PRO 13"),
        (ed.Text(lowercase=True), "Easybook Pro 13", "easybook pro 13"),
        (ed.Text(title=True), "Easybook Pro 13", "Easybook Pro 13"),
        (ed.Text(capitalize=True), "Easybook pro 13", "Easybook pro 13"),
    ],
)
def test_text(parser, test_data, result):
    assert parser.parse(test_data) == result


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.Str(), "Easybook Pro 13", "Easybook Pro 13"),
        (ed.Str(), "easybook pro 13", "easybook pro 13"),
        (ed.Str(), " easybook pro   13", "easybook pro 13"),
        (ed.Str(), "Easybook Pro\n13", "Easybook Pro\n13"),
        (
            ed.Str(),
            "Easybook Pro 13 &lt;3 uÌˆnicode",
            "Easybook Pro 13 &lt;3 uÌˆnicode",
        ),
    ],
)
def test_str(parser, test_data, result):
    assert parser.parse(test_data) == result
