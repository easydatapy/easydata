.. _`parsers-choice`:

==============
Choice Parsers
==============

Choice
======
.. autoclass:: easydata.parsers.choice::Choice

``Choice`` is a parser which will select predetermined value based on search key
matches in a lookup string extracted by a parser.

.. _parsers-choice-getting-started:

Getting Started
---------------
Lets first create our choice parser.

.. code-block:: python

    import easydata as ed


    choice_parser = ed.Choice(
        lookup_parsers=[
            ed.Text(ed.jp('title'))
        ],
        choices = [
            # specified search keys are not case sensitive
            ("accessory", ["phone case", "watch strap"]),
            ("phone", ["mobile", "phone"]),
            ("watch", "watch"),

            # regex pattern as a search key is also acceptable
            ("monitor", ["r\b22\b"]),

            # we can add multiple choices with same name and first one will be returned
            # whose search key will be matched
            ("accessory", ["charger"])
        ],
        # if default_choice is not specified, then None is returned instead.
        default_choice="unknown"
    )

Lets pass some sample data to our choice parser and see the results.

.. code-block:: python

    >>> choice_parser.parse({"title": "EasyWatch"})
    'watch'

.. code-block:: python

    >>> choice_parser.parse({"title": "22 inch monitor"})
    'monitor'

.. code-block:: python

    >>> choice_parser.parse({"title": "Notebook charger"})
    'accessory'

.. code-block:: python

    >>> choice_parser.parse({"title": "PHONE"})
    'phone'

.. code-block:: python

    >>> choice_parser.parse({"title": "PHONE case"})
    'accessory'

.. code-block:: python

    >>> choice_parser.parse({"title": "some new item"})
    'unknown'

Has parser instead of a search key list
#########################################
Lets use our ``Choice`` parser in a model and demonstrate how a specific choice can have
it's own lookup values with search keys through a ``Has`` parser. ``Has`` parser also
provides different search parameters in order to create more accurate match.

.. note::

    Using *Has* parser as a dedicated lookup for a choice key, probably won't be needed in
    most cases since it's usage is for edge cases and for most situations, a simple list of
    search keys should suffice as seen in examples above.

.. code-block:: python

    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        item_name = ed.Text(ed.jp('name'))

        _item_category = ed.Text(ed.jp('category'))

        item_type = ed.Choice(
            lookup_items=['name', 'category'],
            choices = [
                ("accessory", ["phone case", "watch strap"]),
                ("watch", ed.Has(
                    ed.jp('description'),  # this lookup will only be used for a watch choice

                    # our search keys looking for a match are case sensitive
                    ccontains=['TIMEXXX', 'EASYWATCH']
                )),
            ]
        )

Multiple lookup parameters at the same time
###########################################
We can also specify different types of lookup parameters at the same time as we can
see bellow.

.. code-block:: python

    ...
    item_type = ed.Choice(
        lookup_items=['name'],
        lookup_parsers=[
            ed.Text(ed.jp('category'))
        ],
        lookup_queries=[
            ed.jp('breadcrumbs')
        ],
        choices = [
            ("accessory", ["phone case", "watch strap"]),
            ("watch", ed.Has(
                ed.jp('description'),
                ccontains=['TIMEXXX', 'EASYWATCH']
            )),
            ("phone", ["mobile", "phone"]),
            ("monitor", [r'\b22\s?inch\b']),
            ("accessory", ["charger"])
        ]
    )
    ...

Parameters
----------
.. option:: lookup_parsers

We can specify one or multiple lookup parsers where search keys will look for a match.

.. code-block:: python

        ...
        lookup_parsers=[
            ed.Text(ed.jp('category')),
            ed.Text(ed.jp('title'))
        ]
        ...

.. option:: lookup_queries

Instead of ``lookup_parsers`` we can specify list of query search objects as a
value in a ``lookup_queries`` parameter. Behind the scenes they will be passed
to a ``Text`` parser.

.. code-block:: python

        ...
        lookup_queries=[ed.jp('category'), ed.jp('title')]
        ...

.. option:: lookup_items

When ``Choice`` parser is used in a model beside other item parsers, we can use their
parsed value as a lookup values. To achieve this, we specify ``lookup_items`` parameter
which needs to contain list of one or multiple item names from a model.

.. code-block:: python

    import easydata as ed


    class ProductItemModel(ed.ItemModel):
        item_name = ed.Text(ed.jp('name'))

        _item_category = ed.Text(ed.jp('category'))

        item_type = ed.Choice(
            lookup_items=['name', 'category'],
            choices = [
                ("accessory", ["phone case", "watch strap"]),
                ("watch", "watch"),
            ]
        )

.. option:: choices

``choices`` is a required parameter and receives list of tuples, where first value in a
tuple is a choice value and second value is a list of search keys which will be used under
the hood for a match in a lookup string values that were returned through a specified lookup
params.

Examples of ``choices`` parameter usage is already shown thoroughly in a
:ref:`parsers-choice-getting-started` section.
