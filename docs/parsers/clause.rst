.. _`parsers-clause`:

======
Clause
======

OR
==
.. autoclass:: easydata.parsers.clause::OR

**Example:**

Lets import our easydata module first.

.. code-block:: python

    >>> import easydata as ed

Lets write our ``OR`` parser.

.. code-block:: python

    test_html = '''
        <p class="brand">EasyData</p>
    '''

    or_parser = ed.OR(
        ed.Text(ed.pq('.brand-wrong-selector::text')),
        ed.Text(ed.pq('.brand::text')),
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(or_parser.parse(test_html))

.. code-block:: python

    'EasyData'

First our ``parsers.Text(pq('.brand-wrong-selector::text')),`` output was ``None``,
while next ``Text`` parser in line has produced output, since it's selector was able
to extract data from ``HTML``.

Please note that even if query selector found a match and it's content was still
``None``, then data from the next parser in line would be tried to be parsed.

**Another example:**

.. code-block:: python

    test_html = '''
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    '''

    or_parser = ed.Or(
        ed.Text(ed.pq('#name::text')),
        ed.Text(ed.pq('.brand::text'))
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(or_parser.parse(test_html))

.. code-block:: python

    'Easybook Pro 13'

In this case, data parsed in a first parser was returned, since it's css selector
was able to find this time data and because of that, ``Text`` parser returned a
value. All other parsers further down the line are ignored when first match is found.


WITH
====
.. autoclass:: easydata.parsers.clause::WITH

**Example:**

Lets import our easydata module

.. code-block:: python

    >>> import easydata as ed

Lets write our ``WITH`` parser.

.. code-block:: python

    test_html = '''
        <div id="description">
            <ul class="features">
                <li>Material: aluminium <span>MATERIAL</span></li>
                <li>style: <strong>elegant</strong> is this</li>
                <li>Date added: Fri, 12 Dec 2018 10:55</li>
            </ul>
        </div>
    '''

    with_parser = ed.WITH(
        ed.Sentences(
            ed.pq('#description .features::text'),
            allow=['date added'],
        ),
        ed.DateTimeSearch(),
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(with_parser.parse(test_html))

.. code-block:: python

    '12/12/2018 10:55:00'


SWITCH
======
.. autoclass:: easydata.parsers.clause::SWITCH

examples coming soon ...


IF
==
.. autoclass:: easydata.parsers.clause::IF

examples coming soon ...
