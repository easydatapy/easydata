from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule

import easydata as ed
from easydata.contrib.scrapy import ItemModelCrawlSpider, StackedModel
from scrapy.crawler import CrawlerProcess


class BooksSpider(ItemModelCrawlSpider):
    name = "books"

    start_urls = ["http://books.toscrape.com/"]

    rules = [
        Rule(LinkExtractor(restrict_css=".side_categories .nav-list")),
        Rule(LinkExtractor(restrict_css=".pager")),
        Rule(LinkExtractor(restrict_css=".product_pod"), callback="parse_item_model"),
    ]

    item_model_obj = StackedModel(
        breadcrumbs=ed.TextList(
            ed.pq(".breadcrumb li::text-items"),
            deny=["home"],
        ),
        name=ed.Text(ed.pq_strict(".product_main h1")),
        price=ed.PriceFloat(ed.pq(".price_color")),
        url=ed.Data(source="url"),
        image_urls=ed.UrlList(
            ed.pq("#product_gallery .item img::src-items"),
            domain="books.toscrape.com",
        ),
        stock=ed.Bool(ed.pq(".availability::has_class(instock)")),
        description=ed.Description(
            ed.pq("#product_description ~ p:eq(0)"),
            # remove "...more" since it doesn't do anything
            remove_keys=["...more"],
        ),
        features=ed.Features(
            ed.pq(".table"),
            deny=["Avail"],
        )
    )


if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(BooksSpider)

    process.start()
