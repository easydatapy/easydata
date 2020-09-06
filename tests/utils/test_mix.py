from easydata.utils import mix
from tests.factory import load_html_with_pq, load_json

pq = load_html_with_pq("product")
jd = load_json("product")


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
    assert pq("#nested-name").text() == "GROOVE\nEasybook Pro 13"

    rpq = mix.pq_remove_nodes(pq("#nested-name"), ".nested-brand")

    assert rpq.text() == "Easybook Pro 13"

    # Check if original was still preserved
    assert pq("#nested-name").text() == "GROOVE\nEasybook Pro 13"


def test_multiply_list_values_split_key():
    list_values = ["1-2-3", "4-5", "-6"]

    expected_list_values = ["1", "2", "3", "4", "5", "6"]
    assert mix.multiply_list_values(list_values, "-") == expected_list_values
    assert mix.multiply_list_values(list_values, "|") == list_values


def test_multiply_list_values_multiply_key():
    list_values = ["its-one-s"]

    multiply_keys = ("-one-", ["-one-", "-two-", "-three-"])
    expect_list = ["its-one-s", "its-two-s", "its-three-s"]
    assert (
        mix.multiply_list_values(list_values=list_values, multiply_keys=multiply_keys)
        == expect_list
    )

    multiply_keys = [
        ("-two-", ["-two-", "-one-"]),
        ("-one-", ["-one-", "-two-", "-three-"]),
    ]
    assert (
        mix.multiply_list_values(list_values=list_values, multiply_keys=multiply_keys)
        == expect_list
    )
