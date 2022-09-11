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

Each of the ``easydata`` components can be used independently to process data, which
makes writing tests significantly easier. This is is easier because there is not a need
to utilize mocks in testing.

.. topic:: Most important component is a model.

    The Model component glues all of the other components together, parses data, and outputs an item dictionary.


First let create some variables, which will hold different kinds of data, and this will be
passed to a ``parse_item`` method later in this tutorial.

.. code-block:: python

    >> json_text = '{"price": 999.90}'
    >> html_text = '<p class="sale_price">499.9<p>'

First we will create a simple ``ItemModel`` and explain how the data is passed and processed
through other components.

.. code-block:: python

    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        data_processors = [
            ed.DataJsonToDictProcessor()
        ]

        item_price = ed.PriceFloat(ed.jp('price'))

        _item_sale_price = ed.PriceFloat(
            ed.pq('sale_price::text'),
            source='html'
        )

        item_processors = [
            ed.ItemDiscountProcessor()
        ]


.. code-block:: python

    >> product_model = ProductItemModel()

When we initialize our ``ProductItemModel`` nothing happens. Initialization of processors
and other core components is done after we call ``parse_item`` method for a first time.

.. note::

    The design decision to not use ``__init__`` for class initialization is in order to add
    ``ItemModel`` as a mixin to your existing class.

Now lets pass our variables with different types of data to the ``parse_item`` method.

.. code-block:: python

    >> product_model.parse_item(data=json_text, html=html_text)
    {'price': 999.9, 'discount': 50.01}

.. note::

    In the result, we are missing the ``sale_price`` key in our dictionary. This is intentional
    since all properties that start with ``_item`` will be deleted before the final output.

When we pass our ``json_text`` and ``html_text`` to the ``parse_item`` method, our model will get registered
with *model manager* which is in charge of handling are components specified in our model. The model
is registered within *model manager* only when we call the ``parse_item`` method for the first time. In the next
step, the *model manager* is passed through the ``json_text`` and ``html_text`` data will be stored
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

When ``DataBag`` is created under the hood on a ``parse_item`` call, it will be passed
first through **data processors**, where it will be modified or transformed and in next
step will be passed further to item parsers. In item parsers, data will be extracted from
a ``DataBag`` and it's values are stored in a item dictionary.

Before the final output, the item dictionary will get passed through ``item_processors``, and, if needed,
the item dictionary *keys* or *values* will be modified.


Next steps
==========
To get a better understanding regarding processors and many other components, please proceed
further to the :ref:`advanced` section.
