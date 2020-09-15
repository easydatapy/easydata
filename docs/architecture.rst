.. _`architecture`:

============
Architecture
============
``easydata`` consist of several components:

* model
* block models
* parsers
* queries
* data processors
* item processors
* data bag

Each of these components can be used independently to process data and because of that,
writing tests for a custom build components is easy and straightforward without a need
to utilize mocks.

.. topic:: Most important component is a model.

    Model glues all other components together, parses data and outputs item dictionary
    as a result.


First let create some variables, which will hold different kind of data, that will be
passed to a ``parse_item`` method later in this tutorial.

.. code-block:: python

    >> json_text = '{"price": 999.90}'
    >> html_text = '<p class="sale_price">499.9<p>'

First we will create a simple ``ItemModel`` and explain how data is passed and processed
through other components.

.. code-block:: python

    class ProductItemModel(ItemModel):
        data_processors = [
            DataJsonToDictProcessor()
        ]

        item_price = parsers.PriceFloat(jp('price'))

        _item_sale_price = parsers.PriceFloat(
            pq('sale_price::text'),
            source='html'
        )

        item_processors = [
            ItemDiscountProcessor()
        ]


.. code-block:: python

    >> product_model = ProductItemModel()

When we initialize our ``ProductItemModel`` nothing happens. Initialization of processors
and other core components is done after we call ``parse`` method for a first time.

.. note::

    Design decision not to use ``__init__`` for class initialization is in order to add
    ``ItemModel`` as a mixin to your existing class if needed.

Now lets pass our variables with different types of data to ``parse`` method.

.. code-block:: python

    >> product_model.parse(data=json_text, html=html_text)
    {'price': 999.9, 'discount': 50.01}

.. note::

    In a result we are missing ``sale_price`` in our dictionary. This is intentionally
    since all properties that start with ``_item`` will be deleted before final output.

When we pass our ``json_text`` and ``html_text`` to ``parse``, our model will get registered
with *model manager* which basically handles are components specified in our model. Model
is registered within *model manager* only when we call ``parse`` for the first time. In next
step through *model manager* our passed ``json_text`` and ``html_text`` data will be stored
into a ``DataBag`` object dictionary under ``data`` and ``html`` keys respectively. All parsers
and processors will by default look in a ``DataBag`` for a ``data`` key, unless specified
otherwise in a processor or a parser. We can see in our example model above, that a ``PriceFloat``
parser for a ``_item_sale_price`` property has a value ``html`` in it's ``source`` parameter
... this means that under the hood parser will try to extract data from ``html`` key in our
``DataBag`` dictionary rather than default ``data`` key. Similar principles apply also for
data processors.

.. note::

    ``DataBag`` is a dictionary based object, which is used through all parsing cycle in
    a model. All other components (except ``item_processors``) have access to it in
    order to extract, create, modify or delete data in a ``DataBag`` dictionary.

When ``DataBag`` is created under the hood on a ``parse`` call, it will be passed
first through **data processors**, where it will be modified or transformed and in next
step will be passed further to item parsers. In item parsers, data will be extracted from
a ``DataBag`` and it's values stored in a item dictionary.

Before final output, item dictionary will get passed through ``item_processors``, if there is
a need for item dictionary *keys* or *values* to be modified.


Next steps
==========
To get better understanding regarding processors and many other components, please proceed
further to :ref:`advanced` section.
