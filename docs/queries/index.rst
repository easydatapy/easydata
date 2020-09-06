=======
Queries
=======

Queries are modules for data selection from various sources like HTML, XML, JSON, TXT, etc.

Currently easy data has 4 query components, which should cover most of situations.

* :ref:`queries-pyquery` - is a css selector based on package ``pyquery``, which offers
  jquery-like syntax.

* :ref:`queries-jmespath` - is a json selector based on package ``jmespath``, which
  helps you to select deeply nested data with ease. *Please note that on a simple 1 level
  dictionaries, it's preferred to use key query instead due to performance reasons*

* :ref:`queries-key` - is a simple key based selector to be used on a 1 level
  dictionary.

* :ref:`queries-regex` - is a regex based selector with regex pattern as a query.

.. toctree::
    :maxdepth: 2
    :hidden:

    jmespath
    pyquery
    key
    regex
