.. _`advanced`:

========
Advanced
========

Guide Assumptions
=================
This guide is designed for those that already went through :ref:`getting-started`
and :ref:`architecture` sections.


Creating block models
=====================
*Item block models* are ``ItemModel`` objects but with a difference that its
purpose is to be used as a reusable extension that contains predefined item
parsers and processors. To explain this functionality in more details is best
to show it through examples bellow.

Basic block model
-----------------
Lets first create sample *HTML* text stored in a ``test_html`` variable.

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
                <div class="stock" available="Yes">In Stock</div>
            </body>
        </html>
    """

Now let's create model block class, which will be responsible for extracting price
data from the *HTML* above.

.. code-block:: python

    from easydata import ItemModel, parsers
    from easydata.queries import pq


    class PricingBlockModel(ItemModel):
        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        item_processors = [
            ('discount', ItemDiscountProcessor())
        ]

As mentioned before, model blocks as above are meant to be used withing ``ItemModel``.
Now lets create ``ItemModel`` which will utilize ``block_models`` property with
``PricingBlockModel`` as a value in a list.

.. code-block:: python

    from easydata import ItemModel, parsers
    from easydata.queries import pq


    class ProductItemModel(ItemModel):
        block_models = [
            PricingBlockModel()
        ]

        item_name = parsers.Text(
            pq('.name::text'),
        )

        item_brand = parsers.Text(
            pq('.brand::text')
        )

        item_stock = parsers.Bool(
            pq('.stock::attr(available)'),
            contains=['yes']
        )

Now lets parse *HTML* with ``ProductItemModel`` and print it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse(test_html)

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'discount': 50.05,
        'name': 'EasyData Test Product Item',
        'price': 99.9,
        'sale_price': 49.9,
        'stock': True
    }

As we can see from the result, ``discount`` was made through a ``ItemDiscountProcessor``
which was added in a ``PricingBlockModel``.

If needed, we can easily disable ``ItemDiscountProcessor`` within our ``ProductItemModel``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        block_models = [
            PricingBlockModel()
        ]

        item_processors = [
            ('discount', None)
        ]

        ...

We can also override ``item_price`` from the ``PricingBlockModel`` in our ``ProductItemModel``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        block_models = [
            PricingBlockModel()
        ]

        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        ...

Block models with custom parameters
-----------------------------------
We can also create reusable block models with ``__init__`` parameter, which will modify
or create parsers based on our input parameters. This is also preferred way how block
models should be created and used in most cases.

Example:

.. code-block:: python

    from easydata import ItemModel, parsers
    from easydata.queries import pq


    class PricingCssBlockModel(ItemModel):
        def __init__(self,
            price_css,
            sale_price_css,
            calculate_discount = True
        ):

            self.item_price = parsers.PriceFloat(
                pq(price_css)
            )

            self.item_sale_price = parsers.PriceFloat(
                pq(price_css)
            )

            if calculate_discount:
                self.item_processors.append(
                    ('discount', ItemDiscountProcessor())
                )

Now lets use ``PricingCssBlockModel`` in our ``ProductItemModel``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        block_models = [
            PricingCssBlockModel(
                price_css='#price::text',
                sale_price_css='#sale-price::text'
            )
        ]

        ...

Now lets parse *HTML* with ``ProductItemModel`` and print it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse(test_html)

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'discount': 50.05,
        'name': 'EasyData Test Product Item',
        'price': 99.9,
        'sale_price': 49.9,
        'stock': True
    }


Model as item property
======================
Item properties in a model can have instead of a parser object also a ``ItemModel``
object which will produce dictionary value.

In example bellow we will reuse ``PricingCssBlockModel`` from previous section.

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

        item_pricing = PricingCssBlockModel(
            price_css='#price::text',
            sale_price_css='#sale-price::text'
        )

        item_stock = parsers.Bool(
            pq('.stock::attr(available)'),
            contains=['yes']
        )

Now lets parse *HTML* with ``ProductItemModel`` and print it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse(test_html)  # test_html from previous section

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'name': 'EasyData Test Product Item',
        'pricing': {
            'discount': 50.05,
            'price': 99.9,
            'sale_price': 49.9,
        },
        'stock': True
    }


Advanced processor utilization
==============================

Named processors
----------------
We already got to know item and data processors in the :ref:`getting-started`
section and here we will explain how to use named item and data processors from
blocks or models that were dynamically added through a custom model initialization.

For starters lets create *block models* without named item processors.

.. code-block:: python

    class PricingBlockModel(ItemModel):
        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        item_processors = [
            ItemDiscountProcessor()
        ]

Now if we wanted to override ``ItemDiscountProcessor`` in our item model, that
wouldn't be possible. Lets see what happens if we added another ``ItemDiscountProcessor``
with custom parameters in our model.

.. code-block:: python

    class ProductItemModel(ItemModel):
        block_models = [
            PricingBlockModel()
        ]

        item_processors = [
            ItemDiscountProcessor(no_decimals=True)
        ]

        ...

In this case ``ItemDiscountProcessor`` from our ``ProductItemModel`` would be joined
together with the same processor from the ``PricingBlockModel``. For better understanding
lets just show a list how ``item_processors`` behind the scene look like now.

.. code-block:: python

    [
        ItemDiscountProcessor(),
        ItemDiscountProcessor(no_decimals=True)
    ]

As we see there are two ``ItemDiscountProcessor`` while we want only
``ItemDiscountProcessor`` from our model and ignore one from ``PricingBlockModel``.

To solve this issue, named processors are the solution. Lets recreate our
``PricingBlockModel`` but now we will add name to ``ItemDiscountProcessor``.

.. code-block:: python

    class PricingBlockModel(ItemModel):
        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        item_processors = [
            ('discount', ItemDiscountProcessor())
        ]

Now if we want to override in our model, discount item processor from the ``PricingBlockModel``,
we just assign same name to our ``ItemDiscountProcessor`` as it is in ``PricingBlockModel``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        block_models = [
            PricingBlockModel()
        ]

        item_processors = [
            ('discount', ItemDiscountProcessor(no_decimals=True))
        ]

        ...

Now only ``ItemDiscountProcessor`` from our model would get processed.

We can even remove ``ItemDiscountProcessor`` from from the ``PricingBlockModel`` by
adding ``None`` to our named key in ``tuple`` as we can see in example bellow.

.. code-block:: python

    class ProductItemModel(ItemModel):
        block_models = [
            PricingBlockModel()
        ]

        item_processors = [
            ('discount', None)
        ]

        ...

Now discount won't be even calculated.


Protected items
===============
Sometimes we don't want values from item attributes to be outputted in a final
result but we still need them because item processors or other item parsers
rely on them. To solve this issue elegantly, we can just prefix our item properties
with ``_item`` and item with that prefix will be deleted from final output.
Lets demonstrate this in example below.

.. code-block:: python

    class ProductItemModel(ItemModel):
        _item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        _item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        item_processors = [
            ItemDiscountProcessor()
        ]


Now lets parse our ``ProductItemModel`` and print it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse(test_html)  # test_html from previous section

Output:

.. code-block:: python

    {
        'discount': 50.05
    }

As we can see in our result output, that only ``'discount'`` and it's value are returned,
while ``'price'`` and ``'sale_price'`` item keys with it's values got deleted, but only after
they were already processed by item processors.


Item method
===========
In some cases our item parsers just won't parse value from data properly due to
it's complexity and in those cases we can make item methods instead of making parser
instance on a model property.

Lets demonstrate first with a parser instance on a model property to get more clarity.

.. code-block:: python

    class ProductItemModel(ItemModel):
        item_brand = parsers.Text(jp('brand'))

Now in this example instead of defining ``Text`` parser on an item property, we
will create item method which will produce exact same end result.

.. code-block:: python

    class ProductItemModel(ItemModel):
        def item_brand(data: DataBag):
            return data['data']['brand']


Data processing
===============
It's encouraged that you create your own data processors to modify data, so that
custom processors can be reused between other models, but there are some edge
and specific cases which will occur hopefully not often and for that kind of
situations we can override ``preprocess_data`` or ``process_data`` methods from the
``ItemModel`` class. Follow tutorials bellow to get more info regarding these
two methods.

In example bellow we have badly structured json text with missing closing bracket
and because of that it cannot be converted to dict. With ``preprocess_data`` we
can fix it before data is processed by ``data_processors`` and later on, when
json is parsed into dictionary by ``DataJsonToDictProcessor``, we will modify this
dictionary in a ``process_data`` method so that item parsers can use it.

.. code-block:: python

    test_json_text = '{"brand": "EasyData"'

Now lets create our model which will process ``test_json_text`` and utilize
``preprocess_data`` method which will fix bad json in order to be converted
into dictionary by a processor. We will also utilize ``process_data`` which
will create new data source called ``brand_type``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        item_brand = parsers.Text(jp('brand'))

        item_brand_type = parsers.Text(source='brand_type')

        data_processors = [
            DataJsonToDictProcessor()
        ]

        def preprocess_data(self, data):
            data['data'] = data['data'] + '}'
            return data

        def process_data(self, data):
            if 'easydata' in data['data']['brand'].lower():
                data['brand_type'] = 'local'
            else:
                data['brand_type'] = 'other'

            return data

Now lets parse our ``test_json_text`` with ``ProductItemModel`` and show it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse(test_json_text)

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'brand_type': 'local'
    }


Item processing
===============
In a similar way as ``data_processors``, it's encouraged that you create your
own item processors to modify item dictionary, so that custom processors can be
reused between other models, but there are some edge and specific cases which will
occur hopefully not often and for that kind of situations we can override
``preprocess_item`` or ``process_item`` methods from the ``ItemModel`` class.

Follow example bellow to get more info regarding these two methods.

.. code-block:: python

    test_dict = {
        'price': 999.9,
        'sale_price': 1
    }

Now lets create our model which will process our ``test_dict``. With a ``preprocess_item``
we will modify item dictionary before ``item_processors`` are fired so that we can prepare
item in order to be used in  ``item_processors``. In example bellow we will fix wrong sale
price, so that ``ItemDiscountProcessor`` can properly calculate discount and later we will
utilize ``process_item`` method, where new dictionary item ``final_sale`` will be created
with bool value, which is determined if price is discounted or not.

.. code-block:: python

    class ProductItemModel(ItemModel):
        item_price = parsers.PriceFloat(jp('price'))

        _item_sale_price = parsers.PriceFloat(jp('sale_price'))

        item_processors = [
            ItemDiscountProcessor()
        ]

        def preprocess_item(self, item):
            if item['sale_price'] <= 1:
                item['sale_price'] = 0

            return item

        def process_item(self, item):
            item['final_sale'] = bool(item['discount'])

            return item

Now lets parse our ``test_dict`` with ``ProductItemModel`` and show it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse(test_dict)

Output:

.. code-block:: python

    {
        'discount': 0,
        'final_sale': False,
        'price': 999.9
    }

.. note::
    *Please note that sale_price is missing in final output because we declared in
    a model our sale price property as a protected and those get deleted at the end,
    but they are still accessible in ``preprocess_item``, ``item_processors`` and
    ``process_item``.*


Variants
========
*Coming soon ...*


Item Validation
===============
``easydata`` doesn't come with validation solution since it's main purpose is to
transform data, but it's easy to create your own solution via custom item processor
which handles validation or to handle validation after model returns dict item.

Some validation libraries that we recommend:

* Schematics_: validation library based on ORM-like models.
* `JSON Schema`_: validation library based on JSON schema.


.. _`Schematics`: https://schematics.readthedocs.io/en/latest/
.. _`JSON Schema`: https://pypi.org/project/jsonschema/
