.. _`queries-regex`:

=============
ReSearch (re)
=============
.. autoclass:: easydata.queries.re::ReSearch

``ReQuery`` (shortcut: ``re``) allows you to select a value from a text by a *regex* pattern.

Through this tutorial we will use following text which contains some javascript code in it.

.. code-block:: python

    js_text = """
        let spConfig = {
            basePrice: "149.95€",
            prices: {
                basePrice: "0€"
            }
        };
    """

Lets import our easydata module first.

.. code-block:: python

    >>> import easydata as ed

Now lets extract *basePrice* value from our text and pass ``js_text`` to our ``re`` instance.

.. code-block:: python

    >>> ed.re('basePrice: "(.*?)"').get(js_text)
    '149.95€'


Pseudo keys
===========
.. option:: ::all

By default out regex pattern will always return fist match. If we want to get list of all
matches, then we need to add ``::all`` pseudo key to our regex pattern.

    >>> ed.re('basePrice: "(.*?)"::all').get(js_text)
    ['149.95€', '0€']


Parameters
==========

.. option:: dotall

By default is set to ``True``.

.. option:: ignore_case

By default is set to ``False``.

.. option:: bytes_to_string_decode

By default is set to ``'utf-8'``.
