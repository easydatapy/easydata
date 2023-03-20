.. _`parsers-has`:

===
Has
===

Has
===
.. autoclass:: easydata.parsers.has::Has

Getting Started
---------------
``Has`` supports any query object for fetching data.

.. code-block:: python

    >>> ed.Has(ed.jp('info.stock')).parse({'info': {'stock': True}})
    True

In this case if ``jp`` returns ``None``, then bool parser will also return ``False``.

.. code-block:: python

    >>> ed.Has(ed.jp('invalid-key')).parse({})
    False

Use of query selectors is not required, as we can see bellow.

    >>> ed.Bool().parse(True)
    True

Parameters
----------
.. option:: contains

``contains`` property can accept list of keys which will be used for a
match in a lookup text. If match is found then ``True`` is returned. Please
note that search keys are not case sensitive and regex pattern as a key is
also accepted.

.. code-block:: python

    >>> ed.Has(contains=['pro 13']).parse('Easybook Pro 13')
    True

.. option:: ccontains

``ccontains`` works in a same way as ``contains`` parameter, with an exception
that keys are case sensitive.

.. code-block:: python

    >>> ed.Has(contains=['Pro 13']).parse('Easybook Pro 13')
    True

Lets try with lowercase keys.

.. code-block:: python

    >>> ed.Has(contains=['Pro 13']).parse('Easybook Pro 13')
    False

.. option:: contains_query

``contains_query`` is a powerful feature that enables you to specify dynamic
search keys by using query selectors. In example bellow we will use ``jp``
query selector to get our contains keys.

.. code-block:: python

    >>> test_dict = {'title': 'Easybook Pro 13', 'info': {'brand': 'Easybook}'}}
    >>> ed.Has(ed.jp('title'), contains_query=ed.jp('info.brand')).parse(test_dict)
    True


IHas
====
.. autoclass:: easydata.parsers.has::IHas

examples coming soon ...


Bool
====
.. autoclass:: easydata.parsers.has::Bool

examples coming soon ...


IBool
=====
.. autoclass:: easydata.parsers.has::IBool

examples coming soon ...
