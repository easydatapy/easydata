=======
Queries
=======

Queries are modules for data selection from various sources like HTML, XML, JSON, TXT, etc.

Currently easy data has 4 query components, which should cover most of situations.

* :ref:`queries-pyquery` - is a css selector based on package ``pyquery``, which offers
  jquery-like syntax.

* :ref:`queries-jmespath` - is a json selector based on `jmespath`_ package, which
  helps you to select deeply nested data with ease. *Please note that on a simple 1 level
  dictionaries, it's preferred to use key query instead due to performance reasons*

* :ref:`queries-key` - is a simple key based selector to be used on a dictionary.

* :ref:`queries-regex` - is a regex based selector with a regex pattern as a query selector.

* :ref:`queries-cor` - ``or`` clause which can accept 2 or more query selectors and return results
  from the first matching query selector

* :ref:`queries-cwith` - ``with`` clause which can accept 2 or more query selectors and process
  data in a sequence

.. toctree::
    :maxdepth: 2
    :hidden:

    jmespath
    pyquery
    key
    regex
    cor
    cwith


.. _jmespath: https://pypi.org/project/jmespath/
