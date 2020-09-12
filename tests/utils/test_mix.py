import pytest
from pyquery import PyQuery

from easydata.utils import mix

test_nested_html = """
<h2 class="name">
    <div class="brand">EasyData</div>
    Test Product Item
</h2>
"""


def test_unique_list():
    assert mix.unique_list(["a", "a", "b", "c", "c"]) == ["a", "b", "c"]


def test_tuple_list_to_dict():
    test_list = [("Color", "Black"), ("Material", "Plastic"), "Some info"]

    assert mix.tuple_list_to_dict(test_list) == {
        "Color": "Black",
        "Material": "Plastic",
        "Some info": None,
    }


def test_tuple_list_to_dict_default():
    test_list = [("Color", "Black"), "Some info"]

    assert mix.tuple_list_to_dict(test_list, default="") == {
        "Color": "Black",
        "Some info": "",
    }


def test_pq_remove_nodes():
    pq = PyQuery(test_nested_html)

    assert pq(".name").text() == "EasyData\nTest Product Item"

    rpq = mix.pq_remove_nodes(pq(".name"), ".brand")

    assert rpq.text() == "Test Product Item"

    # Check if original was still preserved
    assert pq(".name").text() == "EasyData\nTest Product Item"


@pytest.mark.parametrize(
    "test_data, split_key, result",
    [
        (["1-2-3", "4-5", "-6"], "-", ["1", "2", "3", "4", "5", "6"]),
        (["1-2-3", "4-5", "-6"], "|", ["1-2-3", "4-5", "-6"]),
    ],
)
def test_multiply_list_values_split_key(test_data, split_key, result):
    assert mix.multiply_list_values(test_data, split_key) == result


@pytest.mark.parametrize(
    "multiply_keys",
    [
        ("-one-", ["-one-", "-two-", "-three-"]),
        [
            ("-two-", ["-two-", "-one-"]),
            ("-one-", ["-one-", "-two-", "-three-"]),
        ],
    ],
)
def test_multiply_list_values_multiply_key(multiply_keys):
    multiplied_values = mix.multiply_list_values(
        ["its-one-s"], multiply_keys=multiply_keys
    )

    assert multiplied_values == ["its-one-s", "its-two-s", "its-three-s"]
