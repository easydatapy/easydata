import pytest

from easydata.parsers import Description, Feature, Features, FeaturesDict, Sentences
from tests.factory import data_text


def test_description():
    description_parser = Description()
    expected_text = "Ignored text. Color: Black. Material: Aluminium."
    assert description_parser.parse(data_text.raw_sentences) == expected_text


def test_sentences():
    sentences_parser = Sentences()
    expected_sentences = ["Ignored text.", "Color: Black.", "Material: Aluminium."]
    assert sentences_parser.parse(data_text.raw_sentences) == expected_sentences


def test_features():
    features_parser = Features()
    expected_features = [("Color", "Black"), ("Material", "Aluminium")]
    assert features_parser.parse(data_text.raw_sentences) == expected_features


def test_features_dict():
    features_dict_parser = FeaturesDict()
    expected_features_dict = {"Color": "Black", "Material": "Aluminium"}
    result = features_dict_parser.parse(data_text.raw_sentences)
    assert result == expected_features_dict


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
