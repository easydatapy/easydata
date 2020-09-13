.. _`queries-jmespath`:

===================
JMESPathSearch (jp)
===================
.. autoclass:: easydata.queries.jp::JMESPathSearch

``JMESPathSearch`` (shortcut: ``jp``) allows you to declaratively specify how to extract
elements from a JSON document. ``JMESPathSearch`` uses under the hood the amazing
`jmespath`_ library.

.. note::

    *jp* query works only with dict or list types. If used in a easydata *model*
    and *json* string is provided, then it will try to convert it to a python
    *dict* or *list* under the hood by using *json* module.


Examples:
=========
Through this tutorial we will use following json *dict*:

.. code-block:: python

    test_dict = {
        "title": "EasyBook pro 15",
        "brand": {
            "name": "EasyData",
            "origin": "Slovenia"
        },
        "image_data": [
            {
                "zoom": "https://demo.com/img1.jpg"
            },
            {
                "zoom": "https://demo.com/img2.jpg"
            }
        ],
        "images": [
            "https://demo.com/img1.jpg",
            "https://demo.com/img2.jpg",
            "https://demo.com/img3.jpg"
        ],
        "options": [
            {
                "name": "Monitor",
                "availability": {"value": "yes"},
            },
            {
                "name": "Mouse",
                "availability": {"value": "no"},
            }
        ]
    }

Lets import first our ``jp`` query selector.

.. code-block:: python

    >>> from easydata.queries import jp


**Basic examples**
.. code-block:: python

    >>> jp('title').get(test_dict)
    'EasyBook pro 15'

    >>> jp('brand.name').get(test_dict)
    'EasyData'


**Examples of list**
.. code-block:: python

    >>> jp('images[]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg', 'https://demo.com/img3.jpg']


**Examples of list and slice index**
.. code-block:: python

    >>> jp('images[0:2]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']

    >>> jp('images[:2]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']

    >>> jp('images[1:]').get(test_dict)
    ['https://demo.com/img2.jpg', 'https://demo.com/img3.jpg']

    >>> jp('images[:2]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']


**Example of selecting single value from a list by index**
.. code-block:: python

    >>> jp('images[1]').get(test_dict)
    'https://demo.com/img2.jpg'


**Examples of selecting values from a dict list**
.. code-block:: python

    >>> jp('image_data[].zoom').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']

    >>> jp('image_data[0].zoom').get(test_dict)
    'https://demo.com/img1.jpg'


**Example of list with custom dict values**
.. code-block:: python

    >>> jp('options[].{name: name, stock: availability.value}').get(test_dict)
    [{'name': 'Monitor', 'stock': 'yes'}, {'name': 'Mouse', 'stock': 'no'}]


.. hint::

    In examples above we just saw basic examples how to make JMESPath queries. On
    a `JMESPath website`_ you can learn how to make more advanced queries.


Pseudo keys
===========
.. option:: ::values

``::values`` pseudo key will ensure that only values are selected from a dictionary
and returned as a list.

**Example without *::values* pseudo key**
.. code-block:: python

    >>> jp('brand').get(test_dict)
    {'name': 'EasyData'}


**Example with *::values* pseudo key**
.. code-block:: python

    >>> jp('brand::values').get(test_dict)
    ['EasyData', 'Slovenia']


.. option:: ::keys

``::keys`` pseudo key will ensure that only keys are selected from a dictionary
and returned as a list.

.. code-block:: python

    >>> jp('brand::keys').get(test_dict)
    ['name', 'origin']


.. option:: ::dict(<key>:<value>)

With ``::dict`` we can convert any list of dictionary into a dictionary. ``::dict``
must receive two parameters (*key* and *value*), which are value keys from from a
list of dictionaries.

**Example without *::dict* pseudo key**
.. code-block:: python

    >>> jp('options[].{name: name, stock: availability.value}').get(test_dict)
    [{'name': 'Monitor', 'stock': 'yes'}, {'name': 'Mouse', 'stock': 'no'}]


**Example with *::dict* pseudo key**
.. code-block:: python

    >>> jp('options[].{name: name, stock: availability.value}::dict(name:stock)').get(test_dict)
    {'Monitor': 'yes', 'Mouse': 'no'}


.. _jmespath: https://pypi.org/project/jmespath/
.. _JMESPath website: https://jmespath.org/tutorial.html
