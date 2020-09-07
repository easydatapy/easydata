from easydata import parsers
from easydata.block import Block
from easydata.processors import ItemDiscountProcessor
from easydata.queries import pq


class PricingBlock(Block):
    item_price = parsers.PriceFloat(pq("#price::text"))

    item_sale_price = parsers.PriceFloat(pq("#sale-price::text"))

    items_processors = [("discount", ItemDiscountProcessor())]


class ItemSettingsBlock(Block):
    item_calling_code = 44

    item_country = "UK"
