.. _`getting-started`:

===============
Getting started
===============
This guide covers getting started with the package ``easydata``. After working
through the guide you should know:

    - how to use ``ItemModel``
    - how to assign parsers to ``ItemModel``
    - how to use ``query`` selectors with parsers
    - basic usage of data processors
    - basic usage of item processors

Guide Assumptions
=================
This guide is designed for beginners that haven't worked with ``easydata``
before. There are some prerequisites for the tutorial that have to be
followed:

    - python 3.6 and above
    - installing ``easydata`` package, which can be followed under
      :ref:`installation`

Creating Model
==============
We will use following html in examples bellow:

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

Now lets create an ``ItemModel`` which will process html above and parse it to
item dict. To select data in a text parser we will use ``pq``, which is based
on a PyQuery library and also adds custom pseudo element support like ``::text``,
``attr()``

.. code-block:: python

    from easydata import ItemModel, parsers
    from easydata.queries import pq


    class ProductItemModel(ItemModel):
        item_name = parsers.Text(
            pq('.name::text'),
        )

        item_brand = parsers.Text(
            pq('.brand::text')
        )

        item_description = parsers.Description(
            pq('#description::text')
        )

        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        item_color = parsers.Feature(
            pq('#description::text'),
            key='color'
        )

        item_stock = parsers.Bool(
            pq('.stock::attr(available)'),
            contains=['yes']
        )

        item_images = parsers.List(
            pq('.images img::items'),
            parser=parsers.UrlParser(
                pq('::src')
            )
        )

        """
        Alternative with selecting src values in a first css query:

            item_images = parsers.ListParser(
                pq('.images img::src-items'),
                parser=parsers.UrlParser()
            )
        """


Parsing data with Model
=======================

Calling parse_item to get item dict
-----------------------------------
In example bellow we can see how newly created ``ProductItemModel`` will
parse provided HTML data into ``dict`` object.

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

Calling parse_item from a method inside model
---------------------------------------------
Advantages of calling ``parse_item`` from a method inside a model, is that you
can put all extraction logic (making a request, reading feed file, etc.)
inside item model and have better (depends on a use case) code organization.

.. code-block:: python

    ...
    import json
    import requests


    class ProductItemModel(ItemModel):
        ...
        def store_item_from_url(product_url = None):
            if product_url:
                response = requests.get(product_url)
            else:
                # default url
                response = requests.get('http://demo.com/item-page-123')

            item_data = item_model.parse_item(response.text)

            with open("test_item.txt", "w") as text_file:
                text_file.write(json.dumps(text_file))

Now we can just use our model like this:

    >>> ProductItemModel().store_item_from_url('http://demo.com/item-page-124')

with default url attribute:

    >>> ProductItemModel().store_item_from_url()

and there is no need to call ``parse_item`` on item model object.


Adding Data Processor
=====================
Data processors are extensions to models which help to prepare/convert
data for parser in cases data is more complex and with regular query
selectors it cannot be selected in it's raw form.

.. note::

    **The greatest power of data processor usage is to build your own
    as a reusable piece of data converter in order to be used between
    different models when needed.**

Example
-------
In this example we will use following html with json info:

.. code-block:: python

    test_html = """
        <html>
            <body>
                <h2 class="name">
                    <div class="brand">EasyData</div>
                    Test Product Item
                </h2>
                <script type="text/javascript">
                    var json_data = {
                        "brand": "EasyData",
                        "name": "Test Product Item"
                    };
                </script>
            </body>
        </html>
    """

Lets create our item model with ``data_processors`` included.

.. code-block:: python


    from easydata import ItemModel, parsers
    from easydata.processors import DataJsonFromReToDictProcessor
    from easydata.queries import pq, key


    class ProductItemModel(ItemModel):
        data_processors = [
            DataJsonFromReToDictProcessor(
                r'var json_data = (.*?);',
                new_source='json_info'
            )
        ]

        item_name = parsers.Text(
            key('name'),
            source='json_info'
        )

        item_brand = parsers.Text(
            key('brand'),
            source='json_info'
        )

        item_css_name = parsers.Text(
            pq('.name::text'),
        )

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse_item(test_html)

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'css_name': 'EasyData Test Product Item',
        'name': 'Test Product Item'
    }

How it works
------------
Lets check how ``DataJsonFromReToDictProcessor`` in our example works in more detail.

.. code-block:: python

    data_processors = [
        DataJsonFromReToDictProcessor(
            r'var json_data = (.*?);',
            new_source='json_info'
        )
    ]

First parameter in ``DataJsonFromReToDictProcessor`` is our regex pattern which will
extract json data from our HTML sample above.

Second parameter is ``new_source``. This will tell our processor to store extracted
json data as a separate source and not to overwrite our HTML source. We can see in
our example that item parsers (``item_name`` and ``item_brand``), which are selecting
data from json source, need also ``source`` parameter specified, so that query selectors,
know from which source they need to select/query data.

Example:

.. code-block:: python

    item_name = parsers.TextParser(
        key('name'),
        source='json_info'
    )

If we didn't set ``new_source`` in ``DataJsonFromReToDictProcessor``, then extracted
json data would override default HTML source and bellow case would throw error
because there wouldn't be any HTML data to extract info from.

.. code-block:: python

    item_css_name = parsers.TextParser(
        pq('.name::text'),
    )

We can also specify multiple data processors if needed:

.. code-block:: python

    data_processors = [
        DataJsonFromReToDictProcessor(...),
        DataFromQueryProcessor(...),
    ]

Default data processors
-----------------------
EasyData ships with multiple data processors to handle different case scenarios:

* :ref:`processors-data-processor`
* :ref:`processors-data-to-pq-processor`
* :ref:`processors-data-json-to-dict-processor`
* :ref:`processors-data-json-from-query-to-dict-processor`
* :ref:`processors-data-xml-to-dict-processor`
* :ref:`processors-data-text-from-re-processor`
* :ref:`processors-data-json-from-re-to-dict-processor`
* :ref:`processors-data-from-query-processor`
* :ref:`processors-data-variant-processor`


Adding Item Processor
=====================
Item processors are similar to data processor but instead of transforming data
for a parser, their purpose is to modify already parsed item dictionary.

.. note::

    **Similar to data processors, greatest benefit is to create your own items
    processors and reuse them between different models. For example: validation
    for item dictionary.**

Example
-------
In this example we will use following html:

.. code-block:: python

    test_html = """
        <html>
            <body>
                <h2 class="name">
                    <div class="brand">EasyData</div>
                    Test Product Item
                </h2>
                <div id="price">Was 99.9</div>
                <div id="sale-price">49.9</div>
            </body>
        </html>
    """

Lets create our item model with ``item_processors``

.. code-block:: python

    from easydata import ItemModel, parsers
    from easydata.processors import ItemDiscountProcessor
    from easydata.queries import pq


    class ProductItemModel(ItemModel):
        item_name = parsers.TextParser(
            pq('#name::text', rm='.brand')
        )

        item_brand = parsers.Text(
            pq('.brand::text')
        )

        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        item_processors = [
            ItemDiscountProcessor()
        ]

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse_item(test_html)


Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'name': 'Test Product Item',
        'price': 99.9,
        'sale_price': 49.9,
        'discount': 50.05
    }

How it works
------------
Lets see how ``ItemDiscountProcessor`` works in more detail.

.. code-block:: python

        ...
        item_processors = [
            ItemDiscountProcessor()
        ]

``ItemDiscountProcessor`` looks for parsed ``price`` and ``sale_price`` in item
dictionary and calculates discount between these two values. Finally it creates
a new discount key in item dictionary and adds discount value to it. If our
price and sale price values live under different keys under item dictionary
than default ones ``price`` and ``sale_price``, then we can through parameters
change those default values to suit our needs. All parameters that
``ItemDiscountProcessor`` accepts are ``item_price_key``, ``item_sale_price_key``,
``item_discount_key``, ``decimals``, ``no_decimals``, ``remove_item_sale_price_key``.

We can also specify multiple items processors if needed:

.. code-block:: python

    item_processors = [
        ItemDiscountProcessor(),
        ItemKeysMergeIntoDictProcessor(
            new_item_key='price_info',
            item_keys=['price', 'sale_price', 'discount'],
            preserve_original=False  # will delete keys in item dict
        )
    ]

``item_processors`` in above example would produce following output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'name': 'Test Product Item',
        'price_info': {
            'price': 99.9,
            'sale_price': 49.9,
            'discount': 50.05
        }
    }

Default item processors
-----------------------
EasyData ships with multiple items processors to handle different case scenarios:

* :ref:`processors-item-keys-merge-into-list-processor`
* :ref:`processors-item-keys-merge-processor`
* :ref:`processors-item-keys-merge-into-dict-processor`
* :ref:`processors-item-value-to-str-processor`
* :ref:`processors-item-remove-keys-processor`
* :ref:`processors-item-discount-processor`


Next Steps
==========
It's great to have an understanding how is data shared between components, especially
if you are planing to build custom parsers or processors. For a brief explanation
to see how everything works underneath, please refer to :ref:`architecture` section.

For more advanced features please go to :ref:`advanced` section.
