import pprint

import easydata as ed
from easydata.contrib.requests.models import ItemModel
import requests


class QuotesJsItemModel(ItemModel):

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


quotes_js_item_model = QuotesJsItemModel()


def crawl_quotes(url: str = "http://quotes.toscrape.com/js/"):

    print("Crawling: %s" % url)

    response = requests.get(url)

    for item in quotes_js_item_model.parse_res2items(response):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(item)

    _paginate(response)


def _paginate(response):

    next_page_url = ed.Url(
        ed.pq(".pager .next a::href"),
        domain="quotes.toscrape.com",
    ).parse(response.text)

    if next_page_url:
        crawl_quotes(next_page_url)


if __name__ == "__main__":
    crawl_quotes()
