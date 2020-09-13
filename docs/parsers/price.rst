.. _`parsers-price`:

=============
Price Parsers
=============

PriceFloat
==========
.. autoclass:: easydata.parsers.price::PriceFloat

``PriceFloat`` parser will try to extract prices from a ``str``, ``int`` or
``float`` type values and return them as ``float`` type. It supports price
extraction from various types.

``PriceFloat`` parser is based upon ``Text`` parser and therefore inherits all
parameters from it and it's usage.

To read docs regarding other parameters than the one described here, please go to
:ref:`parsers-text` documentation.

Getting Started
---------------
Lets import first ``parsers`` module and ``jp`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import jp

``PriceFloat`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'price': 'Was 99.9€'}
    >>> parsers.PriceFloat(jp('price')).parse(test_dict)
    99.9

Another example with a ``float`` data source.

.. code-block:: python

    >>> test_dict = {'price': 3330.90}
    >>> parsers.PriceFloat(jp('price')).parse(test_dict)
    3330.9

Parameters
----------
.. option:: decimals

We can manipulate how many ``decimals`` parsed value will be have. By default
this limit is ``2``, but we can change this value with a ``decimals`` parameter.

In this example lets set our value output to 3 decimals.

    >>> test_dict = {'price': '999.91264'}
    >>> parsers.PriceFloat(jp('price'), decimals=3).parse(test_dict)
    999.913

Now lets set it to 0 decimals.

    >>> test_dict = {'price': '999.91264'}
    >>> parsers.PriceFloat(jp('price'), decimals=0).parse(test_dict)
    1000

We can completely disable number rounding to decimals by settings
``decimals`` parameter to ``None``.

    >>> test_text = '999.91264'
    >>> parsers.PriceFloat(decimals=None).parse(test_text)
    999.91264

.. note::

    Default value of *decimals* parameter can be defined through a config variable
    :ref:`config-ed-price-decimals` in a config file or a model.


PriceInt
========
.. autoclass:: easydata.parsers.price::PriceInt

``PriceInt`` works exactly the same as ``PriceFloat`` but returns ``int`` type
instead ``float``.

Getting Started
---------------
Lets import first ``parsers`` module and ``jp`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import jp

``PriceInt`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'price': 'Was 99.9€'}
    >>> parsers.PriceInt(jp('price')).parse(test_dict)
    99

Another example with a ``float`` data source.

.. code-block:: python

    >>> test_dict = {'price': 3330.90}
    >>> parsers.PriceInt(jp('price')).parse(test_dict)
    3330


PriceText
=========
.. autoclass:: easydata.parsers.price::PriceText

``PriceText`` works exactly the same as ``PriceFloat`` but returns ``str`` type
instead ``float``.

Getting Started
---------------
Lets import first ``parsers`` module and ``jp`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import jp

``PriceText`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'price': 'Was 99.9€'}
    >>> parsers.PriceText(jp('price')).parse(test_dict)
    '99.9'

Another example with decimal limit.

.. code-block:: python

    >>> test_dict = {'price': 'Was 3.330,9246'}
    >>> parsers.PriceText(jp('price'), decimals=3).parse(test_dict)
    '3330.925'
