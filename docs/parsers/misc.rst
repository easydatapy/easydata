.. _`parsers-misc`:

====
Misc
====

ConcatText
==========
.. autoclass:: easydata.parsers.misc::ConcatText

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
.. autoclass:: easydata.parsers.misc::JoinList

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
.. autoclass:: easydata.parsers.misc::MergeDict

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
            val_parser=ed.Text()
        ),
        ed.Dict(
            ed.jp('specs'),
            key_parser=ed.Text(),
            val_parser=ed.Text()
        ),
    )

Now lets parse ``test_dict`` data and print our result.

.. code-block:: python

    print(merge_dict_parser.parse(test_dict))

.. code-block:: python

    {'color': 'gold', 'display': 'retina', 'proc': 'i7', 'ram': '16 gb'}


ItemDict
========
.. autoclass:: easydata.parsers.misc::ItemDict

examples coming soon ...


ValueList
=========
.. autoclass:: easydata.parsers.misc::ValueList

examples coming soon ...


StringFormat
============
.. autoclass:: easydata.parsers.misc::StringFormat

examples coming soon ...
