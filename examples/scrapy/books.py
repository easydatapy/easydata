from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule

import easydata as ed
from easydata.contrib.scrapy import ItemModel, ItemModelCrawlSpider
from scrapy.crawler import CrawlerProcess


class BooksSpider(ItemModelCrawlSpider):
    name = "books"

    start_urls = ["http://books.toscrape.com/"]

    rules = [
        Rule(LinkExtractor(restrict_css=".side_categories .nav-list")),
        Rule(LinkExtractor(restrict_css=".pager")),
        Rule(LinkExtractor(restrict_css=".product_pod"), callback="parse_item_model"),
    ]

    class ItemModel(ItemModel):
        item_breadcrumbs = ed.TextList(
            ed.pq(".breadcrumb li::text-items"),
            deny=["home"],
        )

        item_name = ed.Text(ed.pq_strict(".product_main h1"))

        item_price = ed.PriceFloat(ed.pq(".price_color"))

        item_url = ed.Data(source="url")

        item_image_urls = ed.UrlList(
            ed.pq("#product_gallery .item img::src-items"),
            domain="books.toscrape.com",
        )

        item_stock = ed.Bool(ed.pq(".availability::has_class(instock)"))

        item_description = ed.Description(
            ed.pq("#product_description ~ p:eq(0)"),
            # remove "...more" since it doesn't do anything
            remove_keys=["...more"],
        )


if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(BooksSpider)

    process.start()
