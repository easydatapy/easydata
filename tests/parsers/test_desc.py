import pytest

import easydata as ed
from tests.factory import data_html, data_text


@pytest.mark.parametrize(
    "test_text, result",
    [
        (data_text.raw_sentences, "Ignored text. Color: Black. Material: Aluminium."),
        (None, None),
        ("", None),
    ],
)
def test_description(test_text, result):
    assert ed.Description().parse(test_text) == result


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
    assert ed.Description(**params).parse(test_text) == result


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
    assert ed.Sentences().parse(test_text) == result


@pytest.mark.parametrize(
    "test_text, result",
    [
        (data_text.raw_sentences, [("Color", "Black"), ("Material", "Aluminium")]),
        (None, None),
        ("", None),
    ],
)
def test_features(test_text, result):
    assert ed.Features().parse(test_text) == result


@pytest.mark.parametrize(
    "test_text, result",
    [
        (data_text.raw_sentences, {"Color": "Black", "Material": "Aluminium"}),
        (None, None),
        ("", None),
    ],
)
def test_features_dict(test_text, result):
    assert ed.FeaturesDict().parse(test_text) == result


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
    feature_parser = ed.Feature(key=key)
    assert feature_parser.parse(data_text.raw_sentences) == result


def test_feature_html_text_to_sentences_false():
    feature_parser = ed.Features(
        query=ed.pq(".specs2"),
        html_text_to_sentences=False,
    )

    assert feature_parser.parse(data_html.features) == [
        ("Product Type", "Papers"),
        ("Price (dddd. tax)", "£52"),
    ]


@pytest.mark.parametrize(
    "key_exact, result",
    [
        ("color", "Black"),
        ("COLOR", "Black"),
        ("colo", None),
    ],
)
def test_feature_key_exact(key_exact, result):
    feature_parser = ed.Feature(key_exact=key_exact)
    assert feature_parser.parse(data_text.raw_sentences) == result
