.. _`parsers-description`:

===================
Description Parsers
===================

Description parsers by default will remove redundant spaces, capitalize sentences,
fix bad encoding and add stop keys if they are missing in a sentences. They can
also parse html tables into readable sentences and offer many options to manipulate
outcome of parsed sentences.

Sentences
=========

.. autoclass:: easydata.parsers.desc::Sentences

``Sentences`` parser will extract and split sentences from given data source.

Getting Started
---------------

Lets import first ``parsers`` module and ``pq`` instance from ``queries``
selector module. ``pq`` is a css query selector using ``PyQuery`` library under
the hood.

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import pq

In our first example we will show how to parse badly structured text.

    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> parsers.Sentences().parse(test_text)
    ['First sentence...', 'Bad ünicode.', 'HTML entities <3!']

Now lets try with simple ``HTML`` text.

.. code-block:: html

    <div class="description">
        <p><b>this</b> is description.</p>
        <ul id="features">
            <li>* Next-generation Thunderbolt.</li>
            <li>* FaceTime HD camera </li>
        </ul>
    </div>

Lets assume that we loaded ``HTML`` above into ``test_html`` variable.

.. code-block:: python

    >>> parsers.Sentences().parse(test_html)
    ['This is description.', 'Next-generation Thunderbolt.', 'FaceTime HD camera.']

Now lets use ``pq`` selector to select specific html nodes in order to
be processed.

    >>> parsers.Sentences(pq('#features').html()).parse(test_html)
    ['Next-generation Thunderbolt.', 'FaceTime HD camera.']

Another example with ``pq`` selector ignoring specific parts od html nodes.

.. code-block:: python

    >>> parsers.Sentences(pq('.description').rm('#features').html()).parse(test_html)
    ['This is description.']

**Description parsers can also process html tables.**

**Without a header example:**

.. code-block:: html

    <div class="description">
        <p><b>this</b> is description.</p>
        <table>
            <tr>
                <td scope="row">Type</td>
                <td>Easybook Pro</td>
            </tr>
            <tr>
                <td scope="row">Operating system</td>
                <td>etOS</td>
            </tr>
        </table>
    </div>

.. code-block:: python

    >>> parsers.Sentences(pq('.description').html()).parse(test_html)
    ['This is description.', 'Type: Easybook Pro.', 'Operating system: etOS.']

**With a header example:**

.. code-block:: html

    <div class="description">
        <p><b>this</b> is description.</p>
        <table>
            <tr>
                <th>Height</th><th>Width</th><th>Depth</th>
            </tr>
            <tr>
                <td>10</td><td>12</td><td>5</td>
            </tr>
            <tr>
                <td>2</td><td>3</td><td>5</td>
            </tr>
        </table>
    </div>

.. code-block:: python

    >>> parsers.Sentences(pq('.description').html()).parse(test_html)
    ['This is description.', 'Height/Width/Depth: 10/12/5.', 'Height/Width/Depth: 2/3/5.']

.. note::

    When using ``pq`` selector we must always call method ``.html()`` so that
    raw html is passed down to description parser because if we call ``.text()``,
    then all html tags will be stripped down and sentences won't be processed
    correctly because description parsers rely on html nodes when extracting
    and structuring sentences.

language
--------

If we are parsing text in other language than english then we need to
specify language parameter in order to determine to which language our
text belongs to so that sentences are split properly around abbreviations.

.. code-block:: python

    >>> test_text = 'primera oracion? Segunda oración. tercera oración'
    >>> parsers.Sentences(language='es').parse(test_text)
    ['Primera oracion?', 'Segunda oración.', 'Tercera oración.']

Please note that currently only ``en`` and ``es`` language parameter values
are supported. *Support for more is under way*

allow
-----

We can control which sentences we want to get extracted by providing list of
keywords into ``allow`` parameter. Provided keys are not case sensitive.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> parsers.Sentences(allow=['first', 'third']).parse(test_text)
    ['First sentence?', 'Third sentence.']

Regex pattern is also supported as parameter value:

.. code-block:: python

    >>> parsers.Sentences(allow=[r'\bfirst']).parse(test_text)

callow
------

``callow`` is similar to ``allow`` but with exception that provided keys
are case sensitive. Regex pattern as a key is also supported.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> parsers.Sentences(allow=['First', 'Third']).parse(test_text)
    ['Third sentence.']

from_allow
----------

We can skip sentences by providing keys in ``from_allow`` parameter.
Keys are not case sensitive and regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> parsers.Sentences(from_allow=['second']).parse(test_text)
    ['Second txt.', 'Third Txt.', 'FOUR txt.']

from_callow
-----------

``from_callow`` is similar to ``from_allow`` but with exception that
provided keys are case sensitive. Regex pattern as a key is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> parsers.Sentences(from_allow=['Second']).parse(test_text)
    ['Second txt.', 'Third Txt.', 'FOUR txt.']

Lets recreate same example as before but with lowercase key.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> parsers.Sentences(from_allow=['second']).parse(test_text)
    []

to_allow
--------

``to_allow`` is similar to ``from_allow`` but in reverse order. Here
are sentences skipped after provided key is found. Keys are not case
sensitive and regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> parsers.Sentences(to_allow=['four']).parse(test_text)
    ['First txt.', 'Second txt.', 'Third Txt.']

to_callow
---------

``to_callow`` is similar to ``to_allow`` but with exception that
provided keys are case sensitive. Regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> parsers.Sentences(to_callow=['FOUR']).parse(test_text)
    ['First txt.', 'Second txt.', 'Third Txt.']

Lets recreate same example as before but with a lowercase key.

.. code-block:: python

    >>> test_text = 'First txt. Second txt. Third Txt. FOUR txt.'
    >>> parsers.Sentences(to_callow=['four']).parse(test_text)
    ['First txt.', 'Second txt.', 'Third Txt.', 'FOUR txt.']

deny
----

We can control which sentences we don't want to get extracted by providing
list of keywords into ``deny`` parameter. Keys are not case sensitive and
regex pattern is also supported.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> parsers.Sentences(deny=['first', 'third']).parse(test_text)
    ['Second sentence.']

cdeny
-----

``cdeny`` is similar to ``deny`` but with exception that provided keys
are case sensitive. Regex pattern as a key is also supported.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> parsers.Sentences(cdeny=['First', 'Third']).parse(test_text)
    ['First sentence?', 'Second sentence.']

normalize
---------

By default parameter ``normalize`` is set to ``True``. This means that any
bad encoding will be automatically fixed, stops added and line breaks
split into sentences.

.. code-block:: python

    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> parsers.Sentences().parse(test_text)
    ['First sentence...', 'Bad ünicode.', 'HTML entities <3!']

Lets try to set parameter ``normalize`` to ``False`` and see what happens.

.. code-block:: python

    >>> test_text = '  first sentence... Bad uÌˆnicode.   HTML entities &lt;3!'
    >>> parsers.Sentences(normalize=False).parse(test_text)
    ['First sentence...', 'Bad uÌˆnicode.', 'HTML entities &lt;3!']

capitalize
----------

By default all sentences will get capitalized as we can see bellow.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> parsers.Sentences().parse(test_text)
    ['First sentence?', 'Second sentence.', 'third sentence.']

We can disable this behaviour by setting parameter ``capitalize`` to ``False``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> parsers.Sentences(capitalize=False).parse(test_text)
    ['first sentence?', 'Second sentence.', 'third sentence.']

title
-----

We can set our text output to title by setting parameter ``title``
to ``True``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> parsers.Sentences(title=True).parse(test_text)
    'First Sentence? Second Sentence. Third Sentence'

uppercase
---------

We can set our text output to uppercase by setting parameter ``uppercase``
to ``True``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> parsers.Sentences(uppercase=True).parse(test_text)
    ['FIRST SENTENCE?', 'SECOND SENTENCE.', 'THIRD SENTENCE.']

lowercase
---------

We can set our text output to lowercase by setting parameter ``lowercase``
to ``True``.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. third sentence'
    >>> parsers.Sentences(lowercase=True).parse(test_text)
    'first sentence? second sentence. third sentence'

min_chars
---------

By default ``min_chars`` has a value of 5. This means that any sentence that has
less than 5 chars, will be filtered out and not seen at the end result. This
is done to remove ambiguous sentences, especially when extracting text from
html. We can raise or decrease this limit by changing the value of ``min_chars``.

replace_keys
------------

We can replace all chars in a sentences by providing tuple of search key and
replacement char in a ``replace_keys`` parameter. Regex pattern as key is
also supported and search keys are not case sensitive.

.. code-block:: python

    >>> test_text = 'first sentence! - second sentence.  Third'
    >>> parsers.Sentences(replace_keys=[('third', 'Last'), ('nce!', 'nce?')]).parse(test_text)
    ['First sentence?', 'Second sentence.', 'Last.']

remove_keys
-----------

We can remove all chars in sentences by providing list of search keys in a
``replace_keys`` parameter. Regex pattern as key is also supported and keys
are not case sensitive.

.. code-block:: python

    >>> test_text = 'first sentence! - second sentence.  Third'
    >>> parsers.Sentences(remove_keys=['sentence', '!']).parse(test_text)
    ['First.', 'Second.', 'Third.']

replace_keys_raw_text
---------------------

We can replace char values before text is split into sentences. This is
especially useful if we want to fix text before it's parsed and so that
is split into sentences correctly. It accepts ``regex`` as key values in a
``tuple``. Please note that keys are not case sensitive and regex as key
is also accepted.

Lets first show default result with badly structured text without
setting keys into ``replace_keys_raw_text``.

.. code-block:: python

    >>> test_text = 'Easybook pro 15 Color: Gray Material: Aluminium'
    >>> parsers.Sentences().parse(test_text)
    ['Easybook pro 15 Color: Gray Material: Aluminium.']

As we can see from the result is returned as only one sentence
due to missing stop keys (``.``) between sentences. Lets fix this by
adding stop keys into unprocessed text before sentence splitting
happens.

.. code-block:: python

    >>> test_text = 'Easybook pro 15 Color: Gray Material: Aluminium'
    >>> replace_keys = [('Color:', '. Color:'), ('Material:', '. Material:')]
    >>> parsers.Sentences(replace_keys_raw_text=replace_keys).parse(test_text)
    ['Easybook pro 15.', 'Color: Gray.', 'Material: Aluminium.']

remove_keys_raw_text
--------------------

Works similar as ``replace_keys_raw_text``, but instead of providing list
of tuples in order to replace chars, here we provide list of chars to remove
keys. Lets try first on a sentence without setting keys to ``rremove_keys_raw_text``.
Please note that keys are not case sensitive and regex as key is also accepted.

.. code-block:: python

    >>> test_text = 'Easybook pro 15. Color: Gray'
    >>> parsers.Sentences().parse(test_text)
    ['Easybook pro 15.', 'Color: Gray.']

Text above due to stop key ``.`` was split into two sentences. Lets prevent this
by removing color and stop key at the same time and get one sentence instead.

.. code-block:: python

    >>> test_text = 'Easybook pro 15. Color: Gray'
    >>> parsers.Sentences(remove_keys_raw_text=['. color:']).parse(test_text)
    ['Easybook pro 15 Gray.']

split_inline_breaks
-------------------

By default text with chars like ``*``, `` - `` and bullet points would get split
into sentences.

Example:

.. code-block:: python

    >>> test_text = '- first param - second param'
    >>> parsers.Sentences().parse(test_text)
    ['First param.', 'Second param.']

In cases when we want to disable this behaviour, we can set parameter
``split_inline_breaks`` to ``False``.

.. code-block:: python

    >>> test_text = '- first param - second param'
    >>> parsers.Sentences(split_inline_breaks=False).parse(test_text)
    ['- first param - second param.']

Please note that chars like ``.``, ``:``, ``?``, ``!`` are not considered
as inline breaks.

inline_breaks
-------------

In above example we saw how default char breaks work. In cases when we want to
split sentences by different char than default one, we can do so by providing list
of chars into ``inline_breaks`` parameter.

.. code-block:: python

    >>> test_text = '> first param > second param'
    >>> parsers.Sentences(inline_breaks=['>']).parse(test_text)
    ['First param.', 'Second param.']

Regex pattern is also supported as a parameter value:

.. code-block:: python

    >>> parsers.Sentences(inline_breaks=[r'\b>']).parse(test_text)

stop_key
--------

If a sentence is without a stop key at the end, then by default it
will automatically be appended ``.``. Let see this in bellow example:

.. code-block:: python

    >>> test_text = 'First feature <br> second feature?'
    >>> parsers.Sentences().parse(test_text)
    ['First feature.', 'Second feature?']

We can change our default char ``.`` to a custom one by setting our
desired char in a ``stop_key`` parameter.

.. code-block:: python

    >>> test_text = 'First feature <br> second feature?'
    >>> parsers.Sentences(stop_key='!').parse(test_text)
    ['First feature!', 'Second feature?']

text_num_to_numeric
-------------------

We can convert all alpha chars that describe numeric values to actual
numbers by setting ``text_num_to_numeric`` parameter to ``True``.

.. code-block:: python

    >>> test_text = 'First Sentence. Two thousand and three has it. Three Sentences.'
    >>> parsers.Sentences(text_num_to_numeric=True).parse(test_text)
    ['1 Sentence.', '2003 has it.', '3 Sentences.']

If our text is in different language we need to change language value in
our ``language`` parameter. Currently supported languages regarding
``text_num_to_numeric`` are only ``en, es, hi and ru``.

Description
===========

.. autoclass:: easydata.parsers.desc::Description

``Description`` parser accepts all parameters as ``Sentences`` parser and works in
exact same way with only difference, that returned value is ``string`` rather
than a ``list`` of sentences.

sentence_separator
------------------

Behind the scenes sentences are from a text always broken into list and
later on a final output joined together by a separator with a default
value ``' '``.

Lets see default output in example bellow:

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> parsers.Description().parse(test_text)
    First sentence? Second sentence. Third sentence.

Behind the scene simple ``join`` on a list of sentences is performed.

Now lets change default value ``' '`` of ``sentence_separator`` to our
custom one.

.. code-block:: python

    >>> test_text = 'first sentence? Second sentence. Third sentence'
    >>> parsers.Description(sentence_separator=' > ').parse(test_text)
    First sentence? > Second sentence. > Third sentence.

Features
========

.. autoclass:: easydata.parsers.desc::Features

``Features`` parser accepts all parameters as ``Sentences`` parser and works in
exact same way with only difference, that list of features is returned. Features
are basically sentences that have a key - value in it.

Example:

.. code-block:: python

    >>> test_text = '- color: Black - material: Aluminium. Last Sentence'

``- color: Black`` and ``- material: Aluminium.`` are feature sentences since they
contain key and value in it, while ``Last Sentence`` is a regular sentence.

``Features`` parser will try to automatically detect which are regular sentences
and which one are features and will show on a final output only ``list`` of
features. Regular sentences are ignored.

.. code-block:: python

    >>> parsers.Features(test_text).parse(test_text)
    [('Color', 'Black'), ('Material', 'Aluminium')]

FeaturesDict
============

.. autoclass:: easydata.parsers.desc::FeaturesDict

``FeaturesDict`` parser accepts all parameters as ``Features`` parser and works in
exact same way with only difference that dictionary of features is returned instead
a list of tuples.

Example:

.. code-block:: python

    >>> test_text = '- color: Black - material: Aluminium. Last Sentence'
    >>> parsers.FeaturesDict(test_text).parse(test_text)
    {'Color': 'Black', 'Material': 'Aluminium'}
