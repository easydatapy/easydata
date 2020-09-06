from easydata import parsers
from easydata.block import Block
from easydata.processors import ItemDiscountProcessor
from easydata.queries import pq

test_html = """
    <html>
        <body>
            <div id="price">Was 99.9</div>
            <div id="sale-price">49.9</div>
        </body>
    </html>
"""


class PricingBlock(Block):
    item_price = parsers.PriceFloat(pq("#price").text)

    item_sale_price = parsers.PriceFloat(pq("#sale-price").text)

    items_processors = [("discount", ItemDiscountProcessor())]


def test_block_parse_data():
    expected_result = {"discount": 50.05, "price": 99.9, "sale_price": 49.9}
    assert PricingBlock().parse_item(test_html) == expected_result
