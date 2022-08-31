from tests.factory.scrapy import (
    EXPECTED_PRODUCT_ITEM_RESULT,
    EXPECTED_PRODUCT_ITEM_RESULT_SCRAPY_ITEM,
    PRODUCT_ITEM_STACKED_MODEL,
    ProductItem,
    ProductItemModel,
    fake_response,
)


class ProductItemModelWithScrapyItem(ProductItemModel):
    sitem_cls = ProductItem


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


def test_item_model_parse_res2item_with_scrapy_item():
    product_item_model = ProductItemModelWithScrapyItem()

    assert (
        product_item_model.parse_res2item(
            response=fake_response(),
        )
        == EXPECTED_PRODUCT_ITEM_RESULT_SCRAPY_ITEM
    )


def test_item_stacked_model_parse_res2item():
    assert (
        PRODUCT_ITEM_STACKED_MODEL.parse_res2item(
            response=fake_response(),
        )
        == EXPECTED_PRODUCT_ITEM_RESULT
    )
