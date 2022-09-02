import pytest
from pyquery import PyQuery

import easydata as ed


@pytest.mark.parametrize(
    "parser, test_data, result",
    [
        (ed.Count(), [1, 2, 3], 3),
        (ed.Count(), "  ", 2),
        (ed.Count(), "12345", 5),
        (ed.Count(none_as_zero=True), None, 0),
        (ed.Count(), (1, 2, 3, 4), 4),
        (ed.Count(count_bool=True), True, 1),
        (ed.Count(count_bool=True), False, 0),
        (ed.Count(), range(0, 4), 4),
        (
            ed.Count(ed.pq("li::items")),
            PyQuery("<ul><li></li><li></li><li></li></ul>"),
            3,
        ),
        (
            ed.Count(ed.pq("li::text-items")),
            PyQuery("<ul><li>1</li><li>2</li><li>3</li></ul>"),
            3,
        ),
        (
            ed.Count(ed.TextList(ed.pq("li::text-items"))),
            PyQuery("<ul><li>1</li><li>2</li><li>3</li></ul>"),
            3,
        ),
    ],
)
def test_count(parser, test_data, result):
    assert parser.parse(test_data) == result


@pytest.mark.parametrize(
    "parser, test_data",
    [
        (ed.Count(), 1),
        (ed.Count(), 1.14),
        (ed.Count(), False),
        (ed.Count(), True),
        (ed.Count(), None),
        (
            ed.Count(ed.pq("li::iter")),
            PyQuery("<ul><li></li><li></li><li></li></ul>"),
        ),
    ],
)
def test_count_error(parser, test_data):
    with pytest.raises(TypeError):
        parser.parse(test_data)
