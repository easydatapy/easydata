from tests.factory.requests import (
    EXPECTED_PRODUCT_ITEM_RESULT,
    PRODUCT_ITEM_STACKED_MODEL,
    ProductItemModel,
    fake_response,
)


def test_item_model_parse_res2item():
    product_item_model = ProductItemModel()

    assert (
        product_item_model.parse_res2item(
            response=fake_response(),
        )
        == EXPECTED_PRODUCT_ITEM_RESULT
    )


def test_item_model_parse_res2items():
    product_item_model = ProductItemModel()

    assert (
        next(
            product_item_model.parse_res2items(
                response=fake_response(),
            )
        )
        == EXPECTED_PRODUCT_ITEM_RESULT
    )


def test_item_model_parse_res2items_to_json():
    product_item_model = ProductItemModel(to_json=False)

    assert (
        next(
            product_item_model.parse_res2items(
                response=fake_response(),
                to_json=True,
            )
        )
        == EXPECTED_PRODUCT_ITEM_RESULT
    )


def test_item_stacked_model_parse_res2item():
    assert (
        PRODUCT_ITEM_STACKED_MODEL.parse_res2item(
            response=fake_response(),
        )
        == EXPECTED_PRODUCT_ITEM_RESULT
    )
