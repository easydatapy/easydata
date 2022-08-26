import pprint

import easydata as ed
from easydata.contrib.requests.models import ItemModel
import requests


class QuotesItemModel(ItemModel):

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

    _api_url = "https://quotes.toscrape.com/api/quotes?page={}"

    def crawl_quotes(self, page: int = 1):
        url = self._api_url.format(page)

        print("Crawling: %s" % url)

        category_data = requests.get(url).json()

        for item in self.parse_items(category_data):
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(item)

        # Paginate
        if category_data["has_next"]:
            next_page = category_data["page"] + 1

            self.crawl_quotes(page=next_page)


if __name__ == "__main__":
    quotes_item_model = QuotesItemModel()

    quotes_item_model.crawl_quotes()
