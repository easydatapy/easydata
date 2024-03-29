import pytest

from easydata import parsers
from easydata.managers import ModelManager
from easydata.models import ItemModel
from easydata.queries import jp


class SettingsBaseModel(ItemModel):
    ED_DATA_VARIANTS_KEY_NAME = "variants_key_test"

    item_language = "fr"

    item_country = ["FR"]

    item_currency = "EUR"

    item_stock = False


class SettingsModel(ItemModel):
    ED_DATA_VARIANTS_NAME = "variants_test"

    item_language = "en-us"

    item_country = ["US"]

    item_currency = "USD"

    item_domain = "us.demo.com"


class ProductModel(ItemModel):
    ED_DATA_VARIANTS_NAME = "variants_test_override"

    item_language = "en"

    item_tags = ["phones", "ecommerce"]

    _item_brand = parsers.Text(jp("brand"), source="json_data")

    item_designer = parsers.Text(from_item="brand")


def test_model_manager():
    model_manager = ModelManager(ProductModel())
    assert model_manager.item_keys() == ["brand", "designer", "language", "tags"]

    assert isinstance(model_manager.get_item_val("tags"), list)

    assert isinstance(model_manager.get_item_val("brand"), parsers.Text)


def test_model_manager_block_models():
    model = ProductModel()
    model.block_models = [SettingsBaseModel(), SettingsModel()]

    model_manager = ModelManager(model)

    result_keys = [
        "country",
        "currency",
        "language",
        "stock",
        "domain",
        "brand",
        "designer",
        "tags",
    ]
    assert model_manager.item_keys() == result_keys

    item_data = model_manager.items()

    assert item_data["language"] == "en"

    assert item_data["currency"] == "USD"

    assert item_data["country"] == ["US"]

    config_variants = "ED_DATA_VARIANTS_NAME"

    assert model_manager.config[config_variants] == "variants_test_override"

    item_designer_parser = model_manager.get_item_val("designer")

    assert item_designer_parser.config[config_variants] == "variants_test_override"


@pytest.mark.parametrize(
    "item_key, item_value",
    [
        ("country", ["FR"]),
        ("language", "en"),
    ],
)
def test_model_manager_block_models_reverse_order(item_key, item_value):
    model = ProductModel()
    model.block_models = [
        SettingsModel(),
        SettingsBaseModel(),
    ]

    model_manager = ModelManager(model)

    item_data = model_manager.items()

    assert item_data[item_key] == item_value


@pytest.mark.parametrize(
    "item_key, item_value",
    [
        ("country", ["FR"]),
        ("language", "en"),
        ("domain", "us.demo.com"),
        ("stock", False),
    ],
)
def test_model_manager_block_models_nested(item_key, item_value):
    model = ProductModel()
    settings_model = SettingsBaseModel()
    settings_model.block_models = [SettingsModel()]

    model.block_models = [settings_model]

    model_manager = ModelManager(model)

    item_data = model_manager.items()

    assert item_data[item_key] == item_value
