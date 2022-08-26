import pprint

import easydata as ed
from easydata.contrib.requests.models import ItemModel
import requests


class QuotesItemModel(ItemModel):

    data_processors = [
        ed.DataFromIterQueryProcessor(ed.pq(".container .row .quote::iter"))
    ]

    item_author = ed.Text(
        ed.pq(".author"),
        uppercase=True,
    )

    item_tags = ed.TextList(
        ed.pq(".tags .tag::iter"),
        title=True,
    )

    item_quote = ed.Text(
        ed.pq(".text::text"),
        process_value=lambda v, db: v.strip('"'),
    )

    def crawl_quotes(
        self,
        url: str = "https://quotes.toscrape.com/",
    ):

        print("Crawling: %s" % url)

        response = requests.get(url)

        for item in self.parse_res2items(response):
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(item)

        self._paginate(response)

    def _paginate(self, response):
        next_page_url = ed.Url(
            ed.pq(".pager .next a::href"),
            domain="quotes.toscrape.com",
        ).parse(response.text)

        if next_page_url:
            self.crawl_quotes(next_page_url)


if __name__ == "__main__":
    quotes_item_model = QuotesItemModel()

    quotes_item_model.crawl_quotes()
