import easydata as ed
from easydata.contrib.scrapy import ItemModel, ItemModelSpider

from scrapy import Request
from scrapy.crawler import CrawlerProcess


class QuoteItemModel(ItemModel):
    data_processors = [ed.DataFromIterQueryProcessor(ed.jp("quotes"))]

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


class QuotesSpider(ItemModelSpider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]

    item_model_cls = QuoteItemModel

    _api_url = "https://quotes.toscrape.com/api/quotes?page={page}"

    def start_requests(self):
        yield Request(self._api_url.format(page=1))

    def parse(self, response, **kwargs):
        yield from self.parse_item_model(response)

        category_data = response.json()

        # Paginate to next api category page if exists
        if category_data["has_next"]:
            next_page = category_data["page"] + 1

            yield Request(
                url=self._api_url.format(page=next_page),
            )


if __name__ == "__main__":
    process = CrawlerProcess()

    process.crawl(QuotesSpider)

    process.start()
