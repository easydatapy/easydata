.. _`getting-started`:

===============
Getting started
===============
This guide covers getting started with the package ``easydata``. After working
through the guide you should know:

    - how to use ``ItemModel``
    - how to assign parsers to ``ItemModel``
    - how to use ``query`` selectors with parsers
    - basic usage of *data* processors
    - basic usage of *item* processors

Guide Assumptions
=================
This guide is designed for beginners that haven't worked with ``easydata`` before. There
are some prerequisites for the tutorial that have to be followed:

    - python 3.6 and above
    - installing ``easydata`` package, which can be followed under :ref:`installation`

Creating Model
==============
We will use following html in examples below:

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

Now lets create an ``ItemModel`` which will process html above and parse it to item dict.
To select data in a text parser we will use ``pq``, which is based on a *PyQuery* library
with custom pseudo elements to handle output (``::text``, ``::href``, ``::attr(<attr-name>)``,
etc.).

.. note::

    *EasyData* currently ships with 4 *query* selectors to handle various data formats:
        * :ref:`queries-pyquery` - is a *css* selector which can handle *HTML* and *XML*
          data formats.
        * :ref:`queries-jmespath` - is advanced json selector.
        * :ref:`queries-key` - is a simple key based selector to be used on a python *dict*.
        * :ref:`queries-regex` - is a *regex* based selector with a regex pattern as a query
          selector.

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
            parser=ed.Url(
                ed.pq('::src')
            )
        )

        """
        Alternative shortcut to get list of image urls:

            item_images = ed.List(
                ed.pq('.images img::src-items'),
                parser=ed.Url()
            )
        """


Parsing data with Model
=======================

Calling parse to get item dict
-----------------------------------
In the example below we can see how the newly created ``ProductItemModel`` will
parse provided HTML data into a ``dict`` object.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse_item(test_html)

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'description': 'Basic product info. EasyData product is newest and greatest \
                        addition to python world. Color: Black. Material: Aluminium.',
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

Calling parse from a method inside model
---------------------------------------------
Advantages of calling ``parse`` from a method inside a model, is that you
can put all extraction logic (making a request, reading feed file, etc.)
inside item model and have better code organization.

.. code-block:: python

    ...
    import json
    import requests


    class ProductItemModel(ed.ItemModel):
        ...
        def store_item_from_url(product_url = None):
            if product_url:
                response = requests.get(product_url)
            else:
                # default url
                response = requests.get('http://demo.com/item-page-123')

            item_data = item_model.parse_item(response.text)

            with open("test_item.txt", "w") as text_file:
                text_file.write(json.dumps(item_data))

Now we can just use our model like this:

    >>> ProductItemModel().store_item_from_url('http://demo.com/item-page-124')

with default url attribute:

    >>> ProductItemModel().store_item_from_url()

and there is no need to call ``parse`` on item model object.


Adding Data Processor
=====================
Data processors are extensions to models which help to prepare/convert
data for parser in the cases where data is more complex and with regular query
selectors it cannot be selected in it's raw form.

.. tip::

    The greatest power of *data* processor usage is to build your own
    as a reusable piece of data converter in order to be used between
    different models when needed.

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
                        "brand": {"name": "EasyData"},
                        "name": "Test Product Item"
                    };
                </script>
            </body>
        </html>
    """

Lets create our item model with ``data_processors`` included.

.. code-block:: python


    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        data_processors = [
            ed.DataJsonFromReToDictProcessor(
                query=r'var json_data = (.*?);',
                new_source='json_info'
            )
        ]

        item_name = ed.Text(
            ed.jp('name'),
            source='json_info'
        )

        item_brand = ed.Text(
            ed.jp('brand.name'),
            source='json_info'
        )

        item_css_name = ed.Text(
            ed.pq('.name::text'),
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
        ed.DataJsonFromReToDictProcessor(
            query=r'var json_data = (.*?);',
            new_source='json_info'
        )
    ]

The first parameter in ``DataJsonFromReToDictProcessor`` is our regex pattern which will
extract json data from our HTML sample above.

The second parameter is ``new_source``. This will tell our processor to store the extracted
json data as a separate source and not to overwrite our HTML source. We can see in
our example that the item parsers ``item_name`` and ``item_brand``, which are selecting
data from the json source, also need the ``source`` parameter specified, so that the query selectors
know which source they need to select/query data from.

Example:

.. code-block:: python

    item_name = ed.Text(
        ed.key('name'),
        source='json_info'
    )

If we didn't set the ``new_source`` parameter in ``DataJsonFromReToDictProcessor``,
then the extracted json data would override default HTML source and the below case would throw an error
because there wouldn't be any HTML data to extract info from.

.. code-block:: python

    item_css_name = ed.Text(
        ed.pq('.name::text'),
    )

We can also specify multiple data processors if needed:

.. code-block:: python

    data_processors = [
        ed.DataJsonFromReToDictProcessor(...),
        ed.DataFromQueryProcessor(...),
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
* :ref:`processors-data-variants-processor`


Adding Item Processor
=====================
*Item* processors are similar to *data* processor but instead of transforming data
for a parser, their purpose is to modify already parsed item dictionary.

.. tip::

    Similar to *data* processors, the greatest benefit is to create your own *item*
    processors and reuse them across different models. For example, you could implement
    validation for an item dictionary.

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

    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        item_name = ed.Text(
            ed.pq('#name::text', rm='.brand')
        )

        item_brand = ed.Text(
            ed.pq('.brand::text')
        )

        item_price = ed.PriceFloat(
            ed.pq('#price::text')
        )

        item_sale_price = ed.PriceFloat(
            ed.pq('#sale-price::text')
        )

        item_processors = [
            ed.ItemDiscountProcessor()
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
            ed.ItemDiscountProcessor()
        ]

``ItemDiscountProcessor`` looks for the parsed ``price`` and ``sale_price`` values in the item
dictionary and calculates the discount between these two values. Finally it creates a new
discount key in the item dictionary and adds the discount value to it. If our price and sale
price values live under different keys under the item dictionary then the default ones are ``price``
and ``sale_price``. All of the parameters that ``ItemDiscountProcessor`` accepts are ``item_price_key``,
``item_sale_price_key``, ``item_discount_key``, ``decimals``, ``no_decimals``,
``remove_item_sale_price_key``.

We can also specify multiple items processors if needed:

.. code-block:: python

    item_processors = [
        ed.ItemDiscountProcessor(),
        ed.ItemKeysMergeIntoDictProcessor(
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
It's great to have an understanding of how the data is shared between components, especially
if you are planing to build custom parsers or processors. For a brief explanation
to see how everything works underneath, please refer to the :ref:`architecture` section.

For more advanced features please go to the :ref:`advanced` section.
