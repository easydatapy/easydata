from easydata import parsers
from easydata.managers import ModelManager
from easydata.models import ItemModel
from easydata.queries import jp


class SettingsBaseModel(ItemModel):
    ED_DATA_VARIANTS_KEY_NAME = "variants_key_test"

    item_language = "fr"

    item_country = ["FR"]

    item_currency = "EUR"


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

    item_temp_brand = parsers.Text(jp("brand"), source="json_data")

    item_designer = parsers.Text(from_item="brand")


def test_model_manager():
    model_manager = ModelManager(ProductModel())
    assert model_manager.item_keys() == ["designer", "language", "tags", "brand"]

    assert isinstance(model_manager.get_item_val("tags"), list)

    assert isinstance(model_manager.get_item_val("brand"), parsers.Text)


def test_model_manager_model_blocks():
    model = ProductModel()
    model.model_blocks = [SettingsBaseModel(), SettingsModel()]

    model_manager = ModelManager(model)

    result_keys = [
        "country",
        "currency",
        "language",
        "domain",
        "designer",
        "tags",
        "brand",
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


def test_model_manager_model_blocks_reverse_order():
    model = ProductModel()
    model.model_blocks = [
        SettingsModel(),
        SettingsBaseModel(),
    ]

    model_manager = ModelManager(model)

    item_data = model_manager.items()

    assert item_data["country"] == ["FR"]

    assert item_data["language"] == "en"


def test_model_manager_model_blocks_nested():
    model = ProductModel()
    settings_model = SettingsBaseModel()
    settings_model.model_blocks = [SettingsModel()]

    model.model_blocks = [settings_model]

    model_manager = ModelManager(model)

    item_data = model_manager.items()

    assert item_data["country"] == ["FR"]

    assert item_data["language"] == "en"

    assert item_data["domain"] == "us.demo.com"
