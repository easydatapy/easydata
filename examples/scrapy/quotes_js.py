import easydata as ed
from easydata.contrib.scrapy import ItemModel, ItemModelCrawlSpider

from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule


class QuotesSpider(ItemModelCrawlSpider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]

    start_urls = ["http://quotes.toscrape.com/js/"]

    rules = [
        Rule(
            LinkExtractor(restrict_css=".pager"),
            follow=True,
            callback="parse_item_model",
        ),
    ]

    class ItemModel(ItemModel):
        data_processors = [
            ed.DataFromIterQueryProcessor(
                ed.cwith(
                    # extract json data
                    ed.re("var data = (.*?]);"),
                    # return root list of quotes
                    ed.jp("[]"),
                )
            )
        ]

        item_author = ed.Text(
            ed.jp("author.name"),
            uppercase=True,
        )

        item_tags = ed.TextList(
            ed.jp("tags"),
            title=True,
        )

        item_quote = ed.Text(
            ed.jp("text"),
            process_value=lambda v, db: v.strip('"'),
        )


if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(QuotesSpider)

    process.start()
