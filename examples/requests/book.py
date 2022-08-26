import pprint

import easydata as ed
from easydata.contrib.requests.models import ItemModel
import requests


class BookItemModel(ItemModel):
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

    item_features = ed.Features(
        ed.pq(".table"),
        deny=["upc", "Availability"],
    )


if __name__ == "__main__":
    book_item_model = BookItemModel()

    single_book_url = (
        "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    )

    book_item = book_item_model.parse_res2item(
        response=requests.get(single_book_url),
    )

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(book_item)
