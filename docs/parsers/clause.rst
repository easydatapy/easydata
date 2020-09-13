.. _`parsers-clause`:

==============
Clause Parsers
==============

Union
=====
.. autoclass:: easydata.parsers.clause::Union

**Example:**

Lets import first ``parsers`` module and ``pq`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import pq

Lets write our ``Union`` parser.

.. code-block:: python

    test_html = '''
        <p class="brand">EasyData</p>
    '''

    union_parser = parsers.Union(
        parsers.Text(pq('.brand-wrong-selector::text')),
        parsers.Text(pq('.brand::text'))
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(union_parser.parse(test_html))

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

    union_parser = parsers.Union(
        parsers.Text(pq('#name::text')),
        parsers.Text(pq('.brand::text'))
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(union_parser.parse(test_html))

.. code-block:: python

    'Easybook Pro 13'

In this case, data parsed in a first parser was returned, since it's css selector
was able to find this time data and because of that, ``Text`` parser returned a
value. All other parsers further down the line are ignored when first match is found.


With
====
.. autoclass:: easydata.parsers.clause::With

**Example:**

Lets import first ``parsers`` module and ``pq`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import pq

Lets write our ``With`` parser.

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

    with_parser = parsers.With(
        parsers.Sentences(
            pq('#description .features::text'),
            allow=['date added']
        ),
        parsers.DateTimeSearch()
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(with_parser.parse(test_html))

.. code-block:: python

    '12/12/2018 10:55:00'


JoinText
========
.. autoclass:: easydata.parsers.clause::JoinText

``JoinText`` will combine string values of two or more parsers.

**Example:**

Lets import first ``parsers`` module and ``pq`` instance from ``queries`` module.

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import pq

Lets write our ``JoinText`` parser.

.. code-block:: python

    test_html = '''
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    '''

    join_text_parser = parsers.JoinText(
        parsers.Text(pq('#name::text')),
        parsers.Text(pq('.brand::text'))
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(join_text_parser.parse(test_html))

.. code-block:: python

    'EasyData Easybook Pro 13'


JoinList
========
.. autoclass:: easydata.parsers.clause::JoinList

``JoinList`` is similar to ``JoinText`` but instead of joining two ``str``
together, it will join two ``list`` types together.

**Example:**

Lets import first ``parsers`` module and ``jp`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import jp

Lets write our ``JoinList`` parser.

.. code-block:: python

    test_dict = {
        'features': [
            'gold color',
            'retina'
        ],
        'specs': [
            'i7 proc',
            '16 gb'
        ]
    }

    join_list_parser = parsers.JoinList(
        parsers.List(
            jp('features'),
            parser=parsers.Text()
        ),
        parsers.List(
            jp('specs'),
            parser=parsers.Text()
        ),
    )

Now lets parse ``test_dict`` data and print our result.

.. code-block:: python

    print(join_list_parser.parse(test_dict))

.. code-block:: python

    ['gold color', 'retina', 'i7 proc', '16 gb']


JoinDict
========
.. autoclass:: easydata.parsers.clause::JoinDict

``JoinDict`` is similar to ``JoinList`` but instead of joining two ``list``
types together, it will join two ``dict`` types together.

**Example:**

Lets import first ``parsers`` module and ``jp`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import jp

Lets write our ``JoinDict`` parser.

.. code-block:: python

    test_dict = {
        'features': {
            'color': 'gold',
            'display': 'retina'
        },
        'specs': {
            'proc': 'i7',
            'ram': '16 gb'
        }
    }

    join_dict_parser = parsers.JoinDict(
        parsers.Dict(
            jp('features'),
            key_parser=parsers.Text(),
            value_parser=parsers.Text()
        ),
        parsers.Dict(
            jp('specs'),
            key_parser=parsers.Text(),
            value_parser=parsers.Text()
        ),
    )

Now lets parse ``test_dict`` data and print our result.

.. code-block:: python

    print(join_dict_parser.parse(test_dict))

.. code-block:: python

    {'color': 'gold', 'display': 'retina', 'proc': 'i7', 'ram': '16 gb'}


ItemDict
========
.. autoclass:: easydata.parsers.clause::ItemDict

examples coming soon ...


ItemList
========
.. autoclass:: easydata.parsers.clause::ItemList

examples coming soon ...
