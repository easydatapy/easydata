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

Lets import our easydata module first.

.. code-block:: python

    >>> import easydata as ed


**Basic examples**
.. code-block:: python

    >>> ed.jp('title').get(test_dict)
    'EasyBook pro 15'

    >>> ed.jp('brand.name').get(test_dict)
    'EasyData'


**Examples of list**
.. code-block:: python

    >>> ed.jp('images[]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg', 'https://demo.com/img3.jpg']


**Examples of list and slice index**
.. code-block:: python

    >>> ed.jp('images[0:2]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']

    >>> ed.jp('images[:2]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']

    >>> ed.jp('images[1:]').get(test_dict)
    ['https://demo.com/img2.jpg', 'https://demo.com/img3.jpg']

    >>> ed.jp('images[:2]').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']


**Example of selecting single value from a list by index**
.. code-block:: python

    >>> ed.jp('images[1]').get(test_dict)
    'https://demo.com/img2.jpg'


**Examples of selecting values from a dict list**
.. code-block:: python

    >>> ed.jp('image_data[].zoom').get(test_dict)
    ['https://demo.com/img1.jpg', 'https://demo.com/img2.jpg']

    >>> ed.jp('image_data[0].zoom').get(test_dict)
    'https://demo.com/img1.jpg'


**Example of list with custom dict values**
.. code-block:: python

    >>> ed.jp('options[].{name: name, stock: availability.value}').get(test_dict)
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

    >>> ed.jp('brand').get(test_dict)
    {'name': 'EasyData'}


**Example with *::values* pseudo key**
.. code-block:: python

    >>> ed.jp('brand::values').get(test_dict)
    ['EasyData', 'Slovenia']


.. option:: ::keys

``::keys`` pseudo key will ensure that only keys are selected from a dictionary
and returned as a list.

.. code-block:: python

    >>> ed.jp('brand::keys').get(test_dict)
    ['name', 'origin']


.. option:: ::dict(<key>:<value>)

With ``::dict`` we can convert any list of dictionary into a dictionary. ``::dict``
must receive two parameters (*key* and *value*), which are value keys from from a
list of dictionaries.

**Example without *::dict* pseudo key**
.. code-block:: python

    >>> ed.jp('options[].{name: name, stock: availability.value}').get(test_dict)
    [{'name': 'Monitor', 'stock': 'yes'}, {'name': 'Mouse', 'stock': 'no'}]


**Example with *::dict* pseudo key**
.. code-block:: python

    >>> ed.jp('options[].{name: name, stock: availability.value}::dict(name:stock)').get(test_dict)
    {'Monitor': 'yes', 'Mouse': 'no'}

.. option:: ::str

With ``::str`` pseudo key we can convert selected value into a *str* format.

.. code-block:: python

    >>> ed.jp('brand::str').get(test_dict)
    "{'name': 'EasyData', 'origin': 'Slovenia'}"

``::str`` pseudo key can be even used as an extension to another pseudo key.

.. code-block:: python

    >>> ed.jp('brand::values-str').get(test_dict)
    "['EasyData', 'Slovenia']"

``-str`` as an extension will work with following pseudo keys: ``keys``, ``values``, ``dict``.

.. option:: ::json

With ``::json`` pseudo key we can convert selected value into a *json* str format.

.. code-block:: python

    >>> ed.jp('brand::json').get(test_dict)
    '{"name": "EasyData", "origin": "Slovenia"}'

``::json`` pseudo key can be even used as an extension to another pseudo key.

.. code-block:: python

    >>> ed.jp('brand::values-json').get(test_dict)
    '["EasyData", "Slovenia"]'

``-json`` as an extension will work with following pseudo keys: ``keys``, ``values``, ``dict``.

.. option:: ::yaml

With ``::yaml`` pseudo key we can convert selected value into a *yaml* str format.

.. code-block:: python

    >>> ed.jp('brand::yaml').get(test_dict)
    'name: EasyData\norigin: Slovenia\n'

``::yaml`` pseudo key can be even used as an extension to another pseudo key.

.. code-block:: python

    >>> ed.jp('brand::keys-yaml').get(test_dict)
    '- name\n- origin\n'

``-yaml`` as an extension will work with following pseudo keys: ``keys``, ``values``, ``dict``.


.. _jmespath: https://pypi.org/project/jmespath/
.. _JMESPath website: https://jmespath.org/tutorial.html
