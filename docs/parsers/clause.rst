.. _`parsers-clause`:

==============
Clause Parsers
==============

Or
==
.. autoclass:: easydata.parsers.clause::Or

**Example:**

Lets import our easydata module first.

.. code-block:: python

    >>> import easydata as ed

Lets write our ``Or`` parser.

.. code-block:: python

    test_html = '''
        <p class="brand">EasyData</p>
    '''

    or_parser = ed.Or(
        ed.Text(ed.pq('.brand-wrong-selector::text')),
        ed.Text(ed.pq('.brand::text'))
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


With
====
.. autoclass:: easydata.parsers.clause::With

**Example:**

Lets import our easydata module

.. code-block:: python

    >>> import easydata as ed

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

    with_parser = ed.With(
        ed.Sentences(
            ed.pq('#description .features::text'),
            allow=['date added']
        ),
        ed.DateTimeSearch()
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(with_parser.parse(test_html))

.. code-block:: python

    '12/12/2018 10:55:00'


ConcatText
==========
.. autoclass:: easydata.parsers.clause::ConcatText

``ConcatText`` will combine string values of two or more parsers.

**Example:**

.. code-block:: python

    >>> import easydata as ed

Lets write our ``ConcatText`` parser.

.. code-block:: python

    test_html = '''
        <p class="brand">EasyData</p>
        <p id="name">Easybook Pro 13</p>
    '''

    concat_text_parser = ed.ConcatText(
        ed.Text(ed.pq('#name::text')),
        ed.Text(ed.pq('.brand::text'))
    )

Now lets parse ``test_html`` data and print our result.

.. code-block:: python

    print(concat_text_parser.parse(test_html))

.. code-block:: python

    'EasyData Easybook Pro 13'


JoinList
========
.. autoclass:: easydata.parsers.clause::JoinList

``JoinList`` is similar to ``JoinText`` but instead of joining two ``str``
together, it will join two ``list`` types together.

**Example:**

.. code-block:: python

    >>> import easydata as ed

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

    join_list_parser = ed.JoinList(
        ed.List(
            ed.jp('features'),
            parser=parsers.Text()
        ),
        ed.List(
            ed.jp('specs'),
            parser=parsers.Text()
        ),
    )

Now lets parse ``test_dict`` data and print our result.

.. code-block:: python

    print(join_list_parser.parse(test_dict))

.. code-block:: python

    ['gold color', 'retina', 'i7 proc', '16 gb']


MergeDict
=========
.. autoclass:: easydata.parsers.clause::MergeDict

``MergeDict`` is similar to ``JoinList`` but instead of joining two ``list``
types together, it will merge two ``dict`` types together.

**Example:**

.. code-block:: python

    >>> import easydata as ed

Lets write our ``MergeDict`` parser.

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

    merge_dict_parser = ed.MergeDict(
        ed.Dict(
            ed.jp('features'),
            key_parser=ed.Text(),
            value_parser=ed.Text()
        ),
        ed.Dict(
            ed.jp('specs'),
            key_parser=ed.Text(),
            value_parser=ed.Text()
        ),
    )

Now lets parse ``test_dict`` data and print our result.

.. code-block:: python

    print(merge_dict_parser.parse(test_dict))

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
