.. _`parsers-text`:

====
Text
====

Text
====
.. autoclass:: easydata.parsers.text::Text

``Text`` is a parser that normalizes and manipulates simple
texts like titles or similar.

Getting Started
---------------

``Text`` supports query selectors for fetching data.

.. code-block:: python

    >>> test_dict = {'title': 'Easybook pro 13'}
    >>> ed.Text(ed.key('title')).parse(test_dict)
    'Easybook pro 13'

In this example lets process text with bad encoding and multiple spaces
between chars.

.. code-block:: python

    >>> ed.Text().parse('Easybook    Pro 13 &lt;3 uÌˆnicode')
    Easybook Pro 13 <3 ünicode

Floats, integers will get transformed to string automatically.

.. code-block:: python

    >>> ed.Text().parse(123)
    '123'

    >>> ed.Text().parse(123.12)
    '123.12'

Parameters
----------
.. option:: normalize

As seen in example above, text normalization (bad encoding) is
enabled by default through ``normalize`` parameter. Lets set ``normalize``
parameter to ``False`` to disable text normalization.

.. code-block:: python

    >>> ed.Text(normalize=False).parse('Easybook Pro 13 &lt;3 uÌˆnicode')
    Easybook Pro 13 &lt;3 uÌˆnicode

.. option:: capitalize

We can capitalize first character in our string, by setting ``capitalize`` parameter
to ``True``. By default is set to ``False``.

.. code-block:: python

    >>> ed.Text(capitalize=True).parse('easybook PRO 15')
    Easybook PRO 15

.. option:: title

We can set all first chars in a word uppercase while other chars in a word
become lowercase with ``title`` parameter set to ``True``.

.. code-block:: python

    >>> ed.Text(title=True).parse('easybook PRO 15')
    Easybook Pro 15

.. option:: uppercase

We can set all chars in our string to uppercase by ``uppercase``
parameter set to ``True``.

.. code-block:: python

    >>> ed.Text(uppercase=True).parse('easybook PRO 15')
    EASYBOOK PRO 15

.. option:: lowercase

We can set all chars in our string to lowercase by ``lowercase``
parameter set to ``True``.

.. code-block:: python

    >>> ed.Text(lowercase=True).parse('easybook PRO 15')
    easybook pro 15

.. option:: replace_keys

We can replace chars/words in a string through ``replace_chars`` parameter.
``replace_chars`` can accept regex pattern as a lookup key and is not
case sensitive.

.. code-block:: python

    >>> test_text = 'Easybook Pro 15'
    >>> ed.Text(replace_keys=[('pro', 'Air'), ('15', '13')]).parse(test_text)
    Easybook Air 13


.. option:: remove_keys

We can remove chars/words in a string through ``remove_keys`` parameter.
``remove_keys`` can accept regex pattern as a lookup key and is not
case sensitive.

.. code-block:: python

    >>> test_text = 'Easybook Pro 15'
    >>> ed.Text(remove_keys=['easy', 'pro']).parse(test_text)
    book 15


.. option:: split_key

Text can be split by ``split_key``. By default split index is ``0``.

.. code-block:: python

    >>> ed.Text(split_key='-').parse('easybook-pro_13')
    easybook

Lets specify split index through tuple.

.. code-block:: python

    >>> ed.Text(split_key=('-', -1)).parse('easybook-pro_13')
    pro_13

.. option:: split_keys

``split_keys`` work in a same way as ``split_key`` but instead of single
split key it accepts list of keys.

.. code-block:: python

    >>> test_text = 'easybook-pro_13'
    >>> ed.Text(split_keys=[('-', -1), '_']).parse(test_text)
    pro

.. option:: take

With ``take`` parameter we can limit maximum number of chars that are
shown at the end result. Lets see how it works in example bellow.

.. code-block:: python

    >>> ed.Text(take=8).parse('Easybook Pro 13')
    Easybook

.. option:: skip

With ``skip`` parameter we can skip defined number of chars from the start.
Lets see how it works in example bellow.

.. code-block:: python

    >>> ed.Text(skip=8).parse('Easybook Pro 13')
    Pro 13

.. option:: text_num_to_numeric

We can convert all alpha chars that describe numeric values to actual
numbers by setting ``text_num_to_numeric`` parameter to ``True``.

.. code-block:: python

    >>> test_text = 'two thousand and three words for the first time'
    >>> ed.Text(text_num_to_numeric=True).parse(test_text)
    2003 words for the 1 time

If our text is in different language we need to change language value in
our ``language`` parameter. Currently supported languages are only
``en, es, hi and ru``.

.. option:: language

.. option:: fix_spaces

By default all multiple spaces will be removed and left with only single
one between chars. Lets test it in our bellow example:

.. code-block:: python

    >>> ed.Text().parse('Easybook   Pro  15')
    Easybook Pro 15

Now lets change ``fix_spaces`` parameter to ``False`` and see what happens.

.. code-block:: python

    >>> ed.Text(fix_spaces=False).parse('Easybook   Pro  15')
    Easybook   Pro  15

.. option:: escape_new_lines

By default all new line characters are converted to empty space as we can
see in example bellow:

.. code-block:: python

    >>> ed.Text().parse('Easybook\nPro\n15')
    Easybook Pro 15

Now lets change ``escape_new_lines`` parameter to ``False`` and see what happens.

.. code-block:: python

    >>> ed.Text(escape_new_lines=False).parse('Easybook\nPro\n15')
    Easybook\nPro\n15

.. option:: new_line_replacement

If ``escape_new_lines`` is set to ``True``, then by default all new line chars
will be replaced by ``' '`` as seen in upper example. We can change this
default setting by changing value of ``new_line_replacement`` parameter.

.. code-block:: python

    >>> ed.Text(new_line_replacement='<br>').parse('Easybook\nPro\n15')
    Easybook<br>Pro<br>15

.. option:: add_stop

We can add stop char at the end of the string by setting ``add_stop``
parameter to ``True``.

.. code-block:: python

    >>> ed.Text(add_stop=True).parse('Easybook Pro  15')
    Easybook Pro 15.

By default ``.`` is added but we can provide our custom char if needed. Instead
of setting ``add_stop`` parameter to ``True``, we can instead of boolean value
provide char as we can see in example bellow.

.. code-block:: python

    >>> ed.Text(add_stop='!').parse('Easybook Pro  15')
    Easybook Pro 15!

.. option:: separator

.. option:: index

.. option:: strip


Str
===
.. autoclass:: easydata.parsers.text::Str

``Str`` parser is same as ``Text`` parser but with ``add_stop`` and ``add_stop``
set to ``False`` by default and because of that ``Str`` parser is also much performant
with it's default params than ``Text`` parser. Use ``Str`` parser when performance
is critical.

.. code-block:: python

    >>> ed.Str().parse('Easybook\nPro\n15 &lt;3 uÌˆnicode')
    Easybook\nPro\n15 &lt;3 uÌˆnicode
