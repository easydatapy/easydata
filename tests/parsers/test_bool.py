import pytest

import easydata as ed
from tests.factory import data_dict, data_text


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.Bool(), 123, True),
        (ed.Bool(), 123.45, True),
        (ed.Bool(), 0.15, True),
        (ed.Bool(), -0.15, True),
        (ed.Bool(), 0, False),
        (ed.Bool(), "True", True),
        (ed.Bool(), "False", False),
        (ed.Bool(), "true", True),
        (ed.Bool(), "false", False),
        (ed.Bool(), None, False),
        (ed.Bool(ed.key("stock")), data_dict.stock, True),
        (ed.Bool(ed.key("stock2")), data_dict.stock, False),
        (ed.Bool(contains=["pro 13"]), data_text.title, True),
        (ed.Bool(contains=["something", "pro 13"]), data_text.title, True),
        (ed.Bool(contains=["pros 13"]), data_text.title, False),
        (ed.Bool(ccontains=["Pro 13"]), data_text.title, True),
        (ed.Bool(ccontains=["something", "Pro 13"]), data_text.title, True),
        (ed.Bool(ccontains=["pro 13"]), data_text.title, False),
        (
            ed.Bool(
                ed.pq("#full-name::text"),
                contains_query=ed.pq(".brand::text"),
            ),
            "Easybook Pro 13",
            False,
        ),
        (
            ed.Bool(
                ed.pq("#full-name::text"),
                contains_query=ed.pq(".brand::text-items"),
            ),
            "Easybook Pro 13",
            False,
        ),
        (ed.IBool(), 123, False),
        (ed.IBool(), 123.45, False),
        (ed.IBool(), 0.15, False),
        (ed.IBool(), -0.15, False),
        (ed.IBool(), 0, True),
        (ed.IBool(), "True", False),
        (ed.IBool(), "False", True),
        (ed.IBool(), "true", False),
        (ed.IBool(), "false", True),
    ],
)
def test_bool_various_types(parser, test_data, result):
    assert parser.parse(test_data) is result
