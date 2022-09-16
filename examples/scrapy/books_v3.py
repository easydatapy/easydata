from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

import easydata as ed
from easydata.contrib.scrapy import StackedModel
from scrapy.crawler import CrawlerProcess


class BooksSpider(CrawlSpider):
    name = "books"

    start_urls = ["http://books.toscrape.com/"]

    rules = [
        Rule(LinkExtractor(restrict_css=".side_categories .nav-list")),
        Rule(LinkExtractor(restrict_css=".pager")),
        Rule(LinkExtractor(restrict_css=".product_pod"), callback="parse_items"),
    ]

    def parse_items(self, response):
        return StackedModel(
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
            stock=ed.Has(ed.pq(".availability::has_class(instock)")),
            description=ed.Description(
                ed.pq("#product_description ~ p:eq(0)"),
                # remove "...more" since it doesn't do anything
                remove_keys=["...more"],
            ),
        ).parse_res2item(response)


if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(BooksSpider)

    process.start()
