.. _`advanced`:

========
Advanced
========

Guide Assumptions
=================
This guide is designed for those that already went through :ref:`getting-started`
and :ref:`architecture` sections.

Creating blocks
===============
``Block`` is similar to ``ItemModel`` but with a difference that its purpose is
to be used as a reusable extension that contains predefined item parsers and
processors. To explain this functionality in more details is best to show it
through examples bellow.

Basic block
-----------
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

Now let's create our ``Block`` class which will be responsible for extracting price
data from the HTML above.

.. code-block:: python

    from easydata import parsers
    from easydata.block import Block
    from easydata.queries import pq


    class PricingBlock(Block):
        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        items_processors = [
            ('discount', ItemDiscountProcessor())
        ]

As mentioned before ``Block`` classes are meant to be used withing ``ItemModel`` so
lets create our ``ItemModel`` bellow.

.. code-block:: python

    from easydata import parsers
    from easydata.models import ItemModel
    from easydata.queries import pq


    class ProductItemModel(ItemModel):
        blocks = [
            PricingBlock()
        ]

        item_name = parsers.TextParser(
            pq('.name::text'),
        )

        item_brand = parsers.TextParser(
            pq('.brand::text')
        )

        item_stock = parsers.BoolParser(
            pq('.stock::attr(available)'),
            contains=['yes']
        )

Now lets parse our HTML with our ``ProductItemModel`` and print it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse_item(test_html)

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
which was added in a ``PricingBlock``.

If needed, we can easily disable ``ItemDiscountProcessor`` in our ``ProductItemModel``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        blocks = [
            PricingBlock()
        ]

        items_processors = [
            ('discount', None)
        ]

        ...

We can also override ``item_price`` from the ``PricingBlock`` in our ``ProductItemModel``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        blocks = [
            PricingBlock()
        ]

        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        ...

Block with custom parameters
----------------------------
We can also create reusable block with ``__init__`` parameters which will
modify or create parsers based on our input parameters. This is also
preferred way how ``blocks`` should be created and used in most cases.

Example:

.. code-block:: python

    from easydata import parsers
    from easydata.block import Block
    from easydata.queries import pq


    class PricingCssBlock(Block):
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

Now lets use ``PricingCssBlock`` in our ``ProductItemModel``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        blocks = [
            PricingCssBlock(
                price_css='#price::text',
                sale_price_css='#sale-price::text'
            )
        ]

        ...


Advanced processor utilization
==============================

Named processors
----------------
We already got to know item and data processors in the :ref:`getting-started`
section and here we will explain how to use named item and data processors from
blocks or models that were dynamically added in a custom model initialization.

For starters lets create ``Block`` without named item processors.

.. code-block:: python

    class PricingBlock(Block):
        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        items_processors = [
            ItemDiscountProcessor()
        ]

Now if we wanted to override ``ItemDiscountProcessor`` in our item model, that
wouldn't be possible. Lets see what happens if we added another ``ItemDiscountProcessor``
with custom parameters in our model.

.. code-block:: python

    class ProductItemModel(ItemModel):
        blocks = [
            PricingBlock()
        ]

        items_processors = [
            ItemDiscountProcessor(no_decimals=True)
        ]

        ...

In this case ``ItemDiscountProcessor`` from our ``ProductItemModel`` would be joined
together with the same processor from the ``PricingBlock``. For better understanding
lets just show a list how ``items_processors`` behind the scene look like now.

.. code-block:: python

    [
        ItemDiscountProcessor(),
        ItemDiscountProcessor(no_decimals=True)
    ]

As we see there are two ``ItemDiscountProcessor`` while we want only
``ItemDiscountProcessor`` from our model and ignore one from ``PricingBlock``.

To solve this issue, named processors are the solution. Lets recreate our
``PricingBlock`` but now we will add name to ``ItemDiscountProcessor``.

.. code-block:: python

    class PricingBlock(Block):
        item_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        items_processors = [
            ('discount', ItemDiscountProcessor())
        ]

Now if we want to override in our model, discount item processor from the ``PricingBlock``,
we just assign same name to our ``ItemDiscountProcessor`` as it is in ``PricingBlock``.

.. code-block:: python

    class ProductItemModel(ItemModel):
        blocks = [
            PricingBlock()
        ]

        items_processors = [
            ('discount', ItemDiscountProcessor(no_decimals=True))
        ]

        ...

Now only ``ItemDiscountProcessor`` from our model would get processed.

We can even remove ``ItemDiscountProcessor`` from from the ``PricingBlock`` by
adding ``None`` to our named key in ``tuple`` as we can see in example bellow.

.. code-block:: python

    class ProductItemModel(ItemModel):
        blocks = [
            PricingBlock()
        ]

        items_processors = [
            ('discount', None)
        ]

        ...

Now discount won't be even calculated.

Temporary item parsers
======================
Sometimes we don't want values from item attributes to be outputted in a final
result but we still need because items processors or other parser rely on them.
To solve this issue elegantly, we can just prefix our attr item names with
``item_temp_`` and item with that prefix will be deleted from final output.
Lets show this in example below.

.. code-block:: python

    class ProductItemModel(ItemModel):
        item_temp_price = parsers.PriceFloat(
            pq('#price::text')
        )

        item_temp_sale_price = parsers.PriceFloat(
            pq('#sale-price::text')
        )

        items_processors = [
            ItemDiscountProcessor()
        ]


Now lets parse our ``ProductItemModel`` and print it's output.

.. code-block:: python

    >>> item_model = ProductItemModel()

    >>> item_model.parse_item(test_html)

Output:

.. code-block:: python

    {
        'discount': 50.05
    }

As we can see only ``'discount'`` and it's value are returned while ``'price'``
and ``'sale_price'`` item keys and it's values gets deleted, but after they are
already passed to item processors in order to be processed.

Item method
===========
In some cases our item parsers just won't parse value from data properly due to
it's complexity and in those cases we can make item methods instead of making an
parser instance on a model property.

Lets demonstrate first parser instance on a model property to get more clarity.

.. code-block:: python

    class ProductItemModel(ItemModel):
        item_brand = parsers.Text(jp('brand'))

Now in this example instead of defining ``Text`` parser on an item property, we
will create item method which will produce exact same end result.

.. code-block:: python

    class ProductItemModel(ItemModel):
        def item_brand(data: DataBag):
            return data['data']['brand']

Data processing in a model
==========================
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

    >>> item_model.parse_item(test_json_text)

Output:

.. code-block:: python

    {
        'brand': 'EasyData',
        'brand_type': 'local'
    }


Item processing in a model
==========================
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
we will modify item dictionary before ``items_processors`` are fired so that we can prepare
item in order to be used in  ``items_processors``. In example bellow we will fix wrong sale
price, so that ``ItemDiscountProcessor`` can properly calculate discount and later we will
utilize ``process_item`` method, where new dictionary item ``final_sale`` will be created
with bool value, which is determined if price is discounted or not.

.. code-block:: python

    class ProductItemModel(ItemModel):
        item_price = parsers.PriceFloat(jp('price'))

        item_temp_sale_price = parsers.PriceFloat(jp('sale_price'))

        items_processors = [
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

    >>> item_model.parse_item(test_dict)

Output:

.. code-block:: python

    {
        'discount': 0,
        'final_sale': False,
        'price': 999.9
    }

.. note::
    *Please note that sale_price is missing in final output because we declared in
    a model our sale price property as a temporary and those get deleted at the end,
    but they are still accessible in ``preprocess_item``, ``items_processors`` and
    ``process_item``.*

Variants
========

*Documentation with examples coming soon ...*

Nesting models
==============

*Documentation with examples coming soon ...*

Validation
==========
``easydata`` doesn't come with validation solution since it's main purpose is to
transform data, but it's easy to create your own solution and bellow we will
explain few of different solutions and best way from our perspective to
implement them.

*Examples coming soon ...*
