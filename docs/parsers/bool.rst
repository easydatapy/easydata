.. _`parsers-bool`:

============
Has Parsers
============

Has
====
.. autoclass:: easydata.parsers.bool::Has

Getting Started
---------------
Lets import our easydata module first.

.. code-block:: python

    >>> import easydata as ed

``Has`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'info': {'stock': True}}
    >>> ed.Has(ed.jp('info.stock')).parse(test_dict)
    True

In this case if ``jp`` returns ``None``, then bool parser will also return ``False``.

.. code-block:: python

    >>> test_dict = {}
    >>> ed.Has(ed.jp('invalid-key')).parse(test_dict)
    False

Use of query selectors is not required, as we can see bellow.

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Has().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().parse(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Has().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().parse(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Has().parse(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Has().parse(test_data)
    True

    >>> test_data = True
    >>> ed.Has().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().parse(test_data)
    True

    >>> test_data = True
    >>> ed.Has().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().parse(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().transform(test_data)
    True

    >>> test_data = True
    >>> ed.Bool().parse(test_data)
    True

Parameters
----------
.. option:: contains

``contains`` property can accept list of keys which will be used for a
match in a lookup text. If match is found then ``True`` is returned. Please
note that search keys are not case sensitive and regex pattern as a key is
also accepted.

.. code-block:: python

    >>> text = 'Easybook Pro 13'
    >>> ed.Has(contains=['pro 13']).parse(text)
    True

.. option:: ccontains

``ccontains`` works in a same way as ``contains`` parameter, with an exception
that keys are case sensitive.

.. code-block:: python

    >>> text = 'Easybook Pro 13'
    >>> ed.Has(contains=['Pro 13']).parse(text)
    True

Lets try with lowercase keys.

.. code-block:: python

    >>> text = 'Easybook Pro 13'
    >>> ed.Has(contains=['Pro 13']).parse(text)
    False

.. option:: contains_query

``contains_query`` is a powerful feature that enables you to specify dynamic
search keys by using query selectors. In example bellow we will use ``jp``
query selector to get our contains keys.

.. code-block:: python

    >>> test_dict = {'title': 'Easybook Pro 13', 'info': {'brand': 'Easybook}'}
    >>> ed.Has(ed.jp('title'), contains_query=ed.jp('info.brand')).parse(text)
    True

.. option:: contains_query_source

``contains_query_source`` will work only when our bool parser is used inside
``model`` in order to select different source from ``data`` object.

.. code-block:: python

    import easydata as ed

    class ProductItemModel(ed.ItemModel):
        item_stock = parsers.Has(
            ed.jp('title'),
            contains_query=ed.jp('name')
            contains_query_source='brand_data'
        )

Now lets test our newly created ``model`` with adding multiple data sources to it.

.. code-block:: python

    >>> test_dict = {'title': 'Easybook Pro 13'}
    >>> test_brand_dict = {'name': 'Easybook'}
    >>> item_model = ProductItemModel().parse(test_dict, brand_data=test_brand_dict)
    {'stock': True}


.. option:: empty_as_false

By default bool parser will always return ``False`` if there is no match or if
given lookup data is empty or contains value of ``None``.

If you need to disable default behaviour and return empty data if given lookup
data is empty, you have to set parameter ``empty_as_false`` to ``False``.

Lets see in example bellow first how default behaviour works.

.. code-block:: python

    >>> test_dict = None
    >>> ed.Has(ed.jp('info.stock')).parse(test_dict)
    False

Lets set ``empty_as_false`` to ``False`` and see what it returns.

.. code-block:: python

    >>> test_dict = None
    >>> ed.Has(ed.jp('info.stock'), empty_as_false=False).parse(test_dict)
    None
