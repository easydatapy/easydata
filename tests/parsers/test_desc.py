import pytest

from easydata.parsers import Description, Feature, Features, FeaturesDict, Sentences
from tests.factory import data_text


@pytest.mark.parametrize(
    "test_text, result",
    [
        (data_text.raw_sentences, "Ignored text. Color: Black. Material: Aluminium."),
        (None, None),
        ("", None),
    ],
)
def test_description(test_text, result):
    assert Description().parse(test_text) == result


@pytest.mark.parametrize(
    "test_text, result, params",
    [
        (data_text.html_sentences, "Title. Hello World! How are u?", {}),
        (data_text.html_sentences, "Hello World!", {"css_query": "p"}),
        (data_text.html_sentences, "Hello World! How are u?", {"exclude_css": "h4"}),
        (data_text.html_sentences, "How are u?", {"exclude_css": ["h4", "p"]}),
        (None, None, {"exclude_css": ["h4", "p"]}),
        ("", None, {"exclude_css": ["h4", "p"]}),
    ],
)
def test_description_html(test_text, result, params):
    assert Description(**params).parse(test_text) == result


@pytest.mark.parametrize(
    "test_text, result",
    [
        (
            data_text.raw_sentences,
            ["Ignored text.", "Color: Black.", "Material: Aluminium."],
        ),
        (None, None),
        ("", None),
    ],
)
def test_sentences(test_text, result):
    assert Sentences().parse(test_text) == result


@pytest.mark.parametrize(
    "test_text, result",
    [
        (data_text.raw_sentences, [("Color", "Black"), ("Material", "Aluminium")]),
        (None, None),
        ("", None),
    ],
)
def test_features(test_text, result):
    assert Features().parse(test_text) == result


@pytest.mark.parametrize(
    "test_text, result",
    [
        (data_text.raw_sentences, {"Color": "Black", "Material": "Aluminium"}),
        (None, None),
        ("", None),
    ],
)
def test_features_dict(test_text, result):
    assert FeaturesDict().parse(test_text) == result


@pytest.mark.parametrize(
    "key, result",
    [
        ("color", "Black"),
        ("COLOR", "Black"),
        ("olor", "Black"),
        ("wrong_key", None),
    ],
)
def test_feature(key, result):
    feature_parser = Feature(key=key)
    assert feature_parser.parse(data_text.raw_sentences) == result


@pytest.mark.parametrize(
    "key_exact, result",
    [
        ("color", "Black"),
        ("COLOR", "Black"),
        ("colo", None),
    ],
)
def test_feature_key_exact(key_exact, result):
    feature_parser = Feature(key_exact=key_exact)
    assert feature_parser.parse(data_text.raw_sentences) == result
