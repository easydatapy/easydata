from easydata.contrib.scrapy import EDSpider
from tests.factory.scrapy import (
    EXPECTED_PRODUCT_ITEM_RESULT,
    EXPECTED_PRODUCT_ITEM_RESULT_SCRAPY_ITEM,
    PRODUCT_ITEM_STACKED_MODEL,
    ProductItemModel,
    fake_response,
)


class DemoSpider(EDSpider):
    name = "demo"


class DemoEDSpider(DemoSpider):
    item_model_cls = ProductItemModel


class DemoInnerClassEDSpider(DemoSpider):
    class ItemModel(ProductItemModel):
        pass


class DemoStackedEDSpider(DemoSpider):
    item_model_obj = PRODUCT_ITEM_STACKED_MODEL


def get_spider_result(spider):
    iter_item = spider.parse_item_model(response=fake_response())

    return next(iter_item)


def test_item_model_spider():
    demo_spider = DemoEDSpider()

    assert get_spider_result(demo_spider) == EXPECTED_PRODUCT_ITEM_RESULT_SCRAPY_ITEM


def test_item_model_spider_with_inner_class():
    demo_spider = DemoInnerClassEDSpider()

    assert get_spider_result(demo_spider) == EXPECTED_PRODUCT_ITEM_RESULT_SCRAPY_ITEM


def test_stacked_item_model_spider():
    demo_spider = DemoStackedEDSpider()

    assert get_spider_result(demo_spider) == EXPECTED_PRODUCT_ITEM_RESULT
