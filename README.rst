========
EasyData
========

.. image:: https://github.com/sitegroove/easydata/workflows/main/badge.svg?style=flat-square
    :target: https://github.com/sitegroove/easydata/actions?query=workflow%3Amain
    :alt: Build status

.. image:: https://readthedocs.org/projects/easydata/badge/?version=latest
    :target: https://easydata.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: code style black

.. image:: https://badge.fury.io/py/easydata.svg?style=flat-square
    :target: https://pypi.org/project/easydata/
    :alt: pypi package version

:warning:

    ``EasyData`` is in early stages of development; backwards incompatible
    changes are possible without deprecation warning until beta status
    is reached and therefore is not suitable to be used in production.


Overview
========
``EasyData`` is data object pattern that provides transformation of item data
from various sources (text, html, xml, json, dictionaries, lists and others) to a
python dictionary with option to even combine different types of sources in order
to transform to dictionary.

It uses component based mapping at the hearth and it's concept is similar to ORM-like
models.


Documentation
=============
Documentation is available online at https://easydata.readthedocs.io/ and in the ``docs``
directory.

The benefits of using EasyData are:
-----------------------------------
* focusing on the object-oriented business logic
* uniform extraction logic between various sources
* speeds up development process of creating a transformer/parser significantly
* time reduction regarding maintenance since it offers clear readability and
  clarity regarding what each components does.
* extraction and parsing logic re-usability
* high and low level option for parsing so that we don't hit any limitations
* option to create custom components for specific needs if needed
* defaults can be changed through configuration on various levels
* creating test cases is a breeze since each component was created to be
  used independently if needed.
* autocomplete works for all parameters on public classes or methods.

Applications:
-------------
* Web scraping. It can easily be integrated with scrapy or any other python
  based solution or even your own.
* Transforming *API* and *FEED* data from various formats.
* Transforming/preparing data for *API* or *FEED*.
* Transforming/preparing data for a database.

.. note::

    EasyData is not tied to any framework, nor it's a framework and it can be
    easily added to existing projects.


Requirements
============
* Python 3.8+
* Works on Linux, Windows, macOS, BSD


Install
=======
The quick way::

    pip install easydata

See the install section in the documentation at
https://easydata.readthedocs.io/en/latest/installation.html for more details.


Example
=======
Bellow we will give just a simple example, so you can get some presentation,
how ``EasyData`` works. For more advanced examples or tutorials please refer
to documentation.

Lets make transformation on a following *HTML*:

.. code-block:: python

    test_html = """
        <html>
            <body>
                <h2 class="name">
                    <div class="brand">EasyData</div>
                    Test Product Item
                </h2>
                <div id="description">
                    <p>Basic product info. EasyData product is newest
                    addition to python <b>world</b></p>
                    <ul>
                        <li>Color: Black</li>
                        <li>Material: Aluminium</li>
                    </ul>
                </div>
                <div id="price">Was 99.9</div>
                <div id="sale-price">49.9</div>
                <div class="images">
                    <img src="http://demo.com/img1.jpg" />
                    <img src="http://demo.com/img2.jpg" />
                    <img src="http://demo.com/img2.jpg" />
                </div>
                <div class="stock" available="Yes">In Stock</div>
            </body>
        </html>
    """

Now lets create an ``ItemModel`` which will process *HTML* above and parse it to
item *dict*.

.. code-block:: python

    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        item_name = ed.Text(
            ed.pq('.name::text'),
        )

        item_brand = ed.Text(
            ed.pq('.brand::text')
        )

        item_description = ed.Description(
            ed.pq('#description::text')
        )

        item_price = ed.PriceFloat(
            ed.pq('#price::text')
        )

        item_sale_price = ed.PriceFloat(
            ed.pq('#sale-price::text')
        )

        item_color = ed.Feature(
            ed.pq('#description::text'),
            key='color'
        )

        item_stock = ed.Has(
            ed.pq('.stock::attr(available)'),
            contains=['yes']
        )

        item_images = ed.List(
            ed.pq('.images img::items'),
            parser=ed.UrlParser(
                ed.pq('::src')
            )
        )

        """
        Alternative with selecting src values in a first css query:

            item_images = ed.ListParser(
                ed.pq('.images img::src-items'),
                parser=ed.UrlParser()
            )
        """

In example bellow we will demonstrate how newly created ``ProductItemModel``
will parse provided *HTML* data into ``dict`` object.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse_item(test_html)

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'description': 'Basic product info. EasyData product is newest addition \
                        to python world. Color: Black. Material: Aluminium.',
        'color': 'Black',
        'images': [
            'http://demo.com/img1.jpg',
            'http://demo.com/img2.jpg',
            'http://demo.com/img3.jpg'
        ],
        'name': 'EasyData Test Product Item',
        'price': 99.9,
        'sale_price': 49.9,
        'stock': True
    }


Contributing
============
**Yes please!**  We are always looking for contributions, additions and improvements.

See https://easydata.readthedocs.io/en/latest/contributing.html for more details.
