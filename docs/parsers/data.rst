.. _`parsers-data`:

====
Data
====

BaseData
========
.. autoclass:: easydata.parsers.base::BaseData

.. note::

    *BaseData* parser can not be instantiated, since it's an abstract class. It's purpose
    is only to be a basis for other parsers that are dependent on querying from a provided
    data.

``BaseData`` parser is most basic parser that accepts only parameters that are related
to selecting data from a provided data source or from other items in a ``model``. All other
parsers except ``clause`` parsers inherit directly ``BaseData`` since it provides logic
to select data with queries from a provided data source and some other features that will be
explained further bellow.

.. hint::
    When you are creating you own parser, you should always inherit from *BaseData*. Best
    reference is to check other parsers how they are build upon *BaseData* and which methods
    are needed to be used in order to process selected value.

Parameters
----------
In bellow examples we will use ``Data`` parser which inherits ``BaseData`` and is exactly
the same as ``BaseData`` since ``BaseData`` can not be instantiated and it's an abstract
class.

.. option:: query

Currently ``EasyData`` has 4 query components, which should cover most of situations.

* :ref:`queries-pyquery` - is a css selector based on package ``pyquery``, which offers
  jquery-like syntax.

* :ref:`queries-jmespath` - is a json selector based on package ``jmespath``, which
  helps you to select deeply nested data with ease. *Please note that on a simple 1 level
  dictionaries, it's preferred to use key query instead due to performance reasons*

* :ref:`queries-key` - is a simple key based selector to be used on a 1 level
  dictionary.

* :ref:`queries-regex` - is a regex based selector with regex pattern as a query.

**Example:**

.. code-block:: python

    >>> import easydata as ed

Lets parse test data ``dict`` with ``Data`` parser.

.. code-block:: python

    >>> test_dict = {'info': {'name': 'EasyBook pro 15'}}
    >>> ed.Data(query=ed.jp('info.name')).parse(test_dict)
    'EasyBook pro 15'

Since ``query`` is first parameter (also in other parsers), we can skip ``query`` key as
we can see bellow.

.. code-block:: python

    >>> ed.Data(ed.jp('info.name')).parse(test_dict)
    'EasyBook pro 15'

We can also specify multiple queries with ``ed.cor`` where data is selected from the
the first matching query.

Now lets create a ``Data`` parser with multiple queries and use ``re`` query which can select
content with regex pattern.

.. code-block:: python

    test_dict = {'info': {'name': 'EasyBook pro 15'}}

    data_parser = ed.Data(
        ed.cor(
            ed.jp('info.name'),
            ed.re(r'\bpro .+'),
        ),
    )

Now lets parse result.

.. code-block:: python

    >>> data_parser.parse(test_dict)
    pro 15

.. option:: from_item

``from_item`` parameter accepts a value of another item parsers name and will get
it's value from there instead in a ``DataBag``.

.. note::
    *from_item* cannot be used in a standalone parser and it will work only if it's used
    in a *model*.

Lets create a ``model`` which will parse HTML data. We will use a ``Has`` parser
as example in this case since it inherits ``Data`` parser.

.. code-block:: python

    test_html = """
        <html>
            <body>
                <h2 class="name">
                    John Doe autographed baseball.
                </h2>
            </body>
        </html>
    """

Now our model:

.. code-block:: python

    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        item_name = ed.Text(
            ed.pq('.name::text'),
        )

        item_signed = ed.Has(
            from_item='name',
            contains=['autographed', 'signed']
        )

Result:

.. code-block:: python

    >>> ProductItemModel().parse_item(test_html)
    {'name': 'John Doe autographed baseball.', 'signed': True}

.. option:: default

Parser can also return ``default`` value if specified, if data cannot be extracted or found
by selectors.

.. code-block:: python

    >>> test_dict = {'info': {'brand': None}}
    >>> ed.Data(query=ed.jp('info.brand'), default='EasyData').parse(test_dict)
    'EasyData'

.. option:: default_from_item

``default_from_item`` works similar to ``default``, but instead of specifying return
value, we specify name of other item parser in a ``model``, from which value will be
taken.

.. note::
    *default_from_item* in a similar way as *from_item* cannot be used in a standalone parser
    and it will work only if it's used in a *model*.

Now as example, lets create a ``model`` which will parse data from a ``dict``.

First ``dict`` with data.

.. code-block:: python

    >>> test_dict = {'info': {'name': 'EasyBook pro 15', 'description': None}}

Now model:

.. code-block:: python

    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        item_name = ed.Text(
            ed.jp('info.name'),
        )

        item_description = ed.Data(
            ed.jp('info.description'),
            default_from_item='name'
        )

Result:

.. code-block:: python

    >>> ProductItemModel().parse_item(test_dict)
    {'name': 'EasyBook pro 15', 'description': 'EasyBook pro 15'}

.. option:: source

``source`` value by default is data of used in a ``model``. This means that by default
parser will always look into ``DataBag`` for a ``data`` key and it's content. If we need
to modify content from a different ``source`` in a ``DataBag``, then we just need to
change ``source`` value.

.. note::
    *source* cannot be used in a standalone parser and it will work only if it's used
    in a *model*.

**Example:**

First let create some variables, which will hold different kind of data, that we will
pass later in this tutorial to a ``parse`` method in a ``model`` instance.

.. code-block:: python

    >>> test_dict = {"brand": "EasyData"}
    >>> test_html = '<p class="name">EasyBook pro 15<p>'

Now we will create a simple ``ItemModel``.

.. code-block:: python

    import easydata as ed

    class ProductItemModel(ed.ItemModel):
        item_brand = ed.Data(ed.jp('brand'))

        item_name = ed.Data(ed.pq('.name'), source="html")

Now lets pass our variables, that we created before, with different kind of data to
``parse`` method and see the result.

.. code-block:: python

    >>> ProductItemModel().parse_item(data=test_dict, html=test_html)
    {'brand': 'EasyData', 'name': 'EasyBook pro 15'}


.. option:: process_raw_value

``process_raw_value`` accepts a callable function. Provided function is fired just after
value is extracted and before value is processed. It's purpose is mostly to prepare value for
processing if needed. Function will receive raw value and data bag parameter. Data bag
parameter will only pass ``DataBag`` object if parser is used in a model, otherwise it's
value will be ``None``.

.. code-block:: python

    test_dict = {'info': {'name': 'EasyBook pro 15'}}
    data_parser = ed.Data(
        ed.jp('info.name'),
        process_raw_value=lambda value, db: "EasyData " + db
    )

Lets parse ``test_dict`` and get our result.

.. code-block:: python

    >>> data_parser.parse(test_dict)
    'EasyData EasyBook pro 15'

.. option:: process_value

``process_value`` accepts a callable function and works in a similar way as
``process_raw_value``. Provided function is fired just before value is outputted and
it's purpose is to add final editing to a value if needed.

.. option:: empty_as_none

.. option:: debug

.. option:: debug_source
