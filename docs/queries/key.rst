.. _`queries-key`:

===============
KeySearch (key)
===============
.. autoclass:: easydata.queries.key::KeySearch

``KeyQuery`` (shortcut: ``key``) allows you to select a value from a dictionary by key.

Lets import our easydata module first.

.. code-block:: python

    >>> import easydata as ed


Examples
========
.. code-block:: python

    >>> test_dict = {"title": "EasyBook pro 15", "brand": {"name": "EasyData"}}

.. code-block:: python

    >>> ed.key('title').get(test_dict)
    'EasyBook pro 15'

.. code-block:: python

    >>> ed.key('brand').get(test_dict)
    {'name': 'EasyData'}


Pseudo keys
===========
.. option:: ::values

``::values`` pseudo key will ensure that only values are selected from a dictionary
and returned as a list.

**Example without *::values* pseudo key**

.. code-block:: python

    >>> {'brand': {'name': 'EasyData', 'origin': 'Slovenia'}}
    >>> ed.key('brand').get(test_dict)
    {'name': 'EasyData', 'origin': 'Slovenia'}


**Example with *::values* pseudo key**

.. code-block:: python

    >>> {'brand': {'name': 'EasyData', 'origin': 'Slovenia'}}
    >>> ed.key('brand::values').get(test_dict)
    ['EasyData', 'Slovenia']


.. option:: ::keys

``::keys`` pseudo key will ensure that only keys are selected from a dictionary
and returned as a list.

.. code-block:: python

    >>> ed.key('brand::keys').get(test_dict)
    ['name', 'origin']

.. option:: ::dict(<key>:<value>)

With ``::dict`` we can convert any list of dictionary into a dictionary. ``::dict``
must receive two parameters (*key* and *value*), which are value keys from from a
list of dictionaries.

We will use following option dictionary in examples bellow:

.. code-block:: python

    >>> odict = {'options': [{'name': 'Monitor', 'stock': 'y'}, {'name': 'Mouse', 'stock': 'n'}]}

**Example without *::dict* pseudo key**

.. code-block:: python

    >>> ed.key('options').get(odict)
    [{'name': 'Monitor', 'stock': 'y'}, {'name': 'Mouse', 'stock': 'n'}]


**Example with *::dict* pseudo key**

.. code-block:: python

    >>> ed.key('options::dict(name:stock)').get(odict)
    {'Monitor': 'y', 'Mouse': 'n'}
