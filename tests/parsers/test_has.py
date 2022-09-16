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
        (ed.Bool(), "true", True),
        (ed.Bool(), "false", True),
        (ed.Bool(), None, False),
        (ed.Bool(), object(), True),
        (ed.Bool(ed.key("stock")), data_dict.stock, True),
        (ed.Bool(ed.key("stock2")), data_dict.stock, False),
        (ed.Bool(), {}, False),
        (ed.Bool(), [], False),
        (ed.Bool(), (), False),
        (ed.Bool(), None, False),
        (ed.Bool(), "", False),
        (ed.IBool(), 123, False),
        (ed.IBool(), 123.45, False),
        (ed.IBool(), 0.15, False),
        (ed.IBool(), -0.15, False),
        (ed.IBool(), 0, True),
        (ed.IBool(), "true", False),
        (ed.IBool(), "false", False),
        (ed.IBool(), {}, True),
        (ed.IBool(), [], True),
        (ed.IBool(), (), True),
        (ed.IBool(), None, True),
        (ed.IBool(), "", True),
    ],
)
def test_bool_various_types(parser, test_data, result):
    assert parser.parse(test_data) is result


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.Has(), 123, True),
        (ed.Has(), 123.45, True),
        (ed.Has(), 0.15, True),
        (ed.Has(), -0.15, True),
        (ed.Has(), 0, False),
        (ed.Has(), "True", True),
        (ed.Has(), "False", False),
        (ed.Has(), "true", True),
        (ed.Has(), "false", False),
        (ed.Has(), None, False),
        (ed.Has(ed.key("stock")), data_dict.stock, True),
        (ed.Has(ed.key("stock2")), data_dict.stock, False),
        (ed.Has(contains=["pro 13"]), data_text.title, True),
        (ed.Has(contains=["something", "pro 13"]), data_text.title, True),
        (ed.Has(contains=["pros 13"]), data_text.title, False),
        (ed.Has(ccontains=["Pro 13"]), data_text.title, True),
        (ed.Has(ccontains=["something", "Pro 13"]), data_text.title, True),
        (ed.Has(ccontains=["pro 13"]), data_text.title, False),
        (ed.Has(), {}, False),
        (ed.Has(), [], False),
        (ed.Has(), None, False),
        (ed.Has(), "", False),
        (
            ed.Has(
                ed.pq("#full-name::text"),
                contains_query=ed.pq(".brand::text"),
            ),
            "Easybook Pro 13",
            False,
        ),
        (
            ed.Has(
                ed.pq("#full-name::text"),
                contains_query=ed.pq(".brand::text-items"),
            ),
            "Easybook Pro 13",
            False,
        ),
        (ed.IHas(), 123, False),
        (ed.IHas(), 123.45, False),
        (ed.IHas(), 0.15, False),
        (ed.IHas(), -0.15, False),
        (ed.IHas(), 0, True),
        (ed.IHas(), "True", False),
        (ed.IHas(), "False", True),
        (ed.IHas(), "true", False),
        (ed.IHas(), "false", True),
        (ed.IHas(), {}, True),
        (ed.IHas(), [], True),
        (ed.IHas(), None, True),
        (ed.IHas(), "", True),
    ],
)
def test_has_various_types(parser, test_data, result):
    assert parser.parse(test_data) is result
