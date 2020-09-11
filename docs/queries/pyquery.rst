.. _`queries-pyquery`:

==================
PyQuerySearch (pq)
==================
.. autoclass:: easydata.queries.pq::PyQuerySearch

``PyQuerySearch`` or it's ``pq`` shortcut is a *css* selector. It uses *PyQuery* library
underneath and on top of that, it adds custom *pseudo keys* witch serve as a command to
determine how selected data will be outputted.

.. note::
    *pq* query selector will also work in most cases with *XML* formats.

Through this tutorial we will use following *HTML*:

.. code-block:: python

    test_html = """
        <html>
            <body>
                <div id="breadcrumbs">
                    <div class=".breadcrumb">Home > </div>
                    <div class=".breadcrumb">Items</div>
                </div>
                <h2 class="name">
                    <div class="brand" content="EasyData">EasyData</div>
                    Test Product Item
                </h2>
                <div class="images">
                    <img src="http://demo.com/img1.jpg" />
                    <img src="http://demo.com/img2.jpg" />
                </div>
                <div class="stock" available="Yes">In Stock</div>
                <input id="stock-quantity" name="quantity" value="12" />
                <a href="https://demo.com" class="link">Home page</a>
            </body>
        </html>
    """

Lets import our ``pq`` query selector. ``pq`` is shortcut for a ``PyQuerySearch`` class.

.. code-block:: python

    >>> from easydata.queries import pq

Now lets select brand name from our *HTML* and pass ``test_html`` to our ``pq`` instance.

.. code-block:: python

    >>> pq('.brand::text').get(test_html)
    'EasyData'

If we wouldn't add pseudo key ``::text`` at the end of our *css* selector, then we would get
``PyQuery`` instance instead of brand value.

Pseudo keys
===========
.. option:: ::text

Pseudo key ``::text`` will ensure that we get always text output. Any *HTML* child elements
will be stripped away and new line breaks will be converted to empty spaces.

Lets select in example bellow ``h2`` element which has a child node ``div``.

.. code-block:: python

    >>> pq('h2::text').get(test_html)
    'EasyData Test Product Item'

.. option:: ::ntext

Pseudo key ``::ntext`` works same as a ``::text`` but with exception that will perform
string normalization. This means that any bad unicode will be fixed ... at least in most
cases.

.. code-block:: python

    >>> bad_html = "<div>uÌˆnicode</div>"
    >>> pq('div::ntext').get(test_html)
    'uÌˆnicode'

.. option:: ::attr(<attr-name>)

With pseudo key ``::attr`` we can select *attributes* in *HTML* elements.

.. code-block:: python

    >>> pq('.brand::attr(content)').get(test_html)
    'EasyData'

.. option:: ::content

Pseudo key ``::content`` is a shortcut for a ``::attr(content)``.

.. code-block:: python

    >>> pq('.brand::content').get(test_html)
    'EasyData'

.. option:: ::href

Pseudo key ``::href`` is a shortcut for a ``::attr(href)``.

.. code-block:: python

    >>> pq('.link::href').get(test_html)
    'EasyData'

.. option:: ::src

Pseudo key ``::src`` is a shortcut for a ``::attr(src)``.

.. code-block:: python

    >>> pq('img::src').get(test_html)
    'http://demo.com/img1.jpg'

.. option:: ::val

Pseudo key ``::val`` is a shortcut for a ``::attr(value)``.

.. code-block:: python

    >>> pq('#stock-quantity::val').get(test_html)
    'EasyData'

.. option:: ::val

Pseudo key ``::name`` is a shortcut for a ``::attr(name)``.

.. code-block:: python

    >>> pq('#stock-quantity::name').get(test_html)
    'quantity'


Pseudo keys "-all" extension
============================
As we can see in out ``test_html`` above, we have multiple elements with a class
value ``breadcrumb``.

Lets try to select them and output it's value with pseudo key ``::text``.

.. code-block:: python

    >>> pq('.breadcrumb::text').get(test_html)
    'Home > '

Pseudo keys will always by default output only first of the selected *HTML* element.

In order to get all elements that matches specified selector, we need to add ``-all`` extension
to our ``::text`` pseudo key. Lets try that in example bellow.

.. code-block:: python

    >>> pq('.breadcrumb::text-all').get(test_html)
    'Home > Items'

``-all`` extension currently works only with ``::text`` and ``::ntext`` pseudo keys.

Pseudo keys "-items" extension
==============================
Purpose of ``-items`` extension is to return a ``list`` of all *HTML* elements matched by
a *css* selector.

.. code-block:: python

    >>> pq('.images img::src-items').get(test_html)
    ['http://demo.com/img1.jpg', 'http://demo.com/img1.jpg']

``-items`` works with all other pseudo keys such as ``::text``, ``::ntext``, ``src``, ``val``,
``::attr(<attr-name>)``, ``href``, etc.

Removing HTML elements from result
==================================
Lets say we have following HTML:

.. code-block:: python

    test_html = """
        <h2>
            <span>EasyData</span>
            Test Product Item
        </h2>
    """

If we wanted to select ``h2`` element and it's content but to exclude content of ``span``
element, then we need to specify ``rm`` property with a css selector that points to an
element that we want to be excluded from end result.

.. code-block:: python

    >>> pq('h2::text', rm='span').get(test_html)
    'Test Product Item'

We can also exclude multiple nested *HTML* elements by separating them with a *comma* if needed.

.. code-block:: python

    >>> pq('h2::text', rm='span,#some-id,.some-class').get(test_html)

