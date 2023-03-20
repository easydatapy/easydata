.. _`parsers-list`:

====
List
====

List
====
.. autoclass:: easydata.parsers.list::List

``List`` parser returns a value of ``list`` type. It's main advantage is that each
value from list can be processed by other parser which is initialized together with
``List`` parser. For better explanation regarding this, please check further through
examples.

Getting Started
---------------
**EXAMPLE WITH JSON DATA SOURCE:**

Lets first try to parse simple json text.

.. code-block:: python

    test_json_text = {
        'images': [
            {'src': 'https://demo.com/imgs/1.jpg'},
            {'src': 'https://demo.com/imgs/2.jpg'},
            {'src': 'https://demo.com/imgs/3.jpg'}
        ]
    }

``List`` supports any query object for fetching data. In example bellow we will
use ``jp`` to query dict object. ``jp`` will also automatically convert our
json text into python ``dictionary`` or ``list`` if it's not already python object.

.. code-block:: python

    list_parser = ed.List(
        ed.jp('images[].src'),
        parser=ed.Url()
    )

    print(list_parser.parse(test_json_text))


This would print output like:

.. code-block:: python

    test_json_text = [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg',
        'https://demo.com/imgs/3.jpg'
    ]

We can also use selector in our ``Url`` parser if needed. Lets demonstrate this in
example bellow.

.. code-block:: python

    list_parser = ed.List(
        ed.jp('images'),
        parser=ed.Url(
            ed.jp('src')
        )
    )

    print(list_parser.parse(test_json_text))

Printed results is also same as before.

.. code-block:: python

    [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg',
        'https://demo.com/imgs/3.jpg'
    ]

**EXAMPLE WITH HTML DATA SOURCE:**

Now lets try to parse simple ``HTML`` text.

.. code-block:: html

    <div id="image-container">
        <img id="image" src="https://demo.com/imgs/1.jpg">
        <div id="images">
            <img class="image" src="https://demo.com/imgs/1.jpg">
            <img class="image" src="https://demo.com/imgs/2.jpg">
            <img class="image" src="https://demo.com/imgs/3.jpg">
        </div>
    </div>

Lets assume that we loaded ``HTML`` above into ``test_html_text`` variable.

In example bellow we will use ``pq`` to query through html nodes. ``pq``
will also automatically convert our ``HTML`` text into python ``PyQuery``
object through which we can use css selectors.

.. code-block:: python

    list_parser = ed.List(
        ed.pq('#images img::items'),
        parser=ed.Url(ed.pq('::src'))
    )

Please note that ``pq('#images img::items')`` will be iterated through our ``List``
parser and that img html node object will be passed to ``Url`` parser upon which
``pq`` query selector can be used again to output final result. Since in example
above in our ``List`` parser, we already selected with css img html node, so in
``Url`` parser we just add into query selector ``::src`` pseudo element in order
to get data from ``src`` attribute in HTML element.

Now lets parse ``test_html_text`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_html_text))

.. code-block:: python

    [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg',
        'https://demo.com/imgs/3.jpg'
    ]

Parameters
----------
.. option:: unique

By default ``List`` parser will ensure that all values in a returned ``list``
are unique and that there are no duplicate values.

Lets first try to parse json text that contains duplicate image urls.

First we will demonstrate default behaviour which has by default ``unique``
parameter set to ``True``.

.. code-block:: js

    {
        'images': [
            'https://demo.com/imgs/1.jpg'
            'https://demo.com/imgs/2.jpg',
            'https://demo.com/imgs/3.jpg',
            'https://demo.com/imgs/3.jpg'
        ]
    }

.. code-block:: python

    list_parser = ed.List(
        ed.jp('images'),
        parser=ed.Url()
    )

Now lets parse ``test_json_text`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_json_text))

.. code-block:: python

    [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg',
        'https://demo.com/imgs/3.jpg'
    ]

As we can see, all our printed ``list`` values are unique. Now lets set ``unique``
parameter to ``False`` and see what happens.

.. code-block:: python

    list_parser = ed.List(
        ed.jp('images'),
        parser=ed.Url(),
        unique=False
    )

Now lets parse ``test_json_text`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_json_text))

.. code-block:: python

    [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg',
        'https://demo.com/imgs/3.jpg',
        'https://demo.com/imgs/3.jpg'
    ]

As we can see our list contains now two ``https://demo.com/imgs/3.jpg`` values.

.. option:: max_num

Setting a ``int`` value to ``max_num`` parameter will basically ensure how many
values we want in our end ``list`` result.

.. code-block:: python

    test_image_list = [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg',
        'https://demo.com/imgs/3.jpg'
    ]

    list_parser = ed.List(
        parser=ed.Url(),
        max_num=2
    )

Now lets parse ``test_image_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg'
    ]

As we can see, our original ``list`` had 3 image urls in it, and now because we have
set to our parameter ``max_num`` value of 2, we get only ``list`` consisted of 2
image urls.

.. option:: split_key

Through ``split_key`` we can break a text into list which be processed by ``List``
parser.

Example:

.. code-block:: python

    test_text = 'https://demo.com/imgs/1.jpg,https://demo.com/imgs/2.jpg'

    list_parser = ed.List(
        parser=ed.Url(),
        split_key=','
    )

Now lets parse ``test_text`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg'
    ]

.. option:: allow_parser

.. option:: deny_parser


TextList
========
.. autoclass:: easydata.parsers.list::TextList

``TextList`` extends ``List`` parsers and therefore all parameters from it, are also
available in ``TextList``. ``TextList`` output is a ``list`` of ``str``.

Parameters
----------
.. option:: allow

We can control which list values we want to get extracted by providing list of
keywords into ``allow`` parameter. Provided keys are not case sensitive and regex
pattern as a key is also supported.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        allow=['.com', '.eu']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'http://demo.com',
        'http://demo.eu'
    ]

.. option:: callow

``callow`` is similar to ``allow`` but with exception that provided keys
are case sensitive. Regex pattern as a key is also supported.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        callow=['.COM', '.eu']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'http://demo.eu'
    ]

.. option:: from_allow

We can skip list values by providing keys in ``from_allow`` parameter.
Keys are not case sensitive and regex pattern is also supported.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        from_allow=['.net']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'http://demo.net',
        'http://demo.eu'
    ]

.. option:: from_callow

``from_callow`` is similar to ``from_allow`` but with exception that
provided keys are case sensitive. Regex pattern as a key is also supported.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        from_callow=['.net']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'http://demo.net',
        'http://demo.eu'
    ]

Lets recreate same example as before but with uppercase key.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        from_callow=['.net']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    []

.. option:: to_allow

``to_allow`` is similar to ``from_allow`` but in reverse order. Here
are list values skipped after provided key is found. Keys are not case
sensitive and regex pattern is also supported.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        to_allow=['.eu']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'http://demo.com',
        'http://demo.net'
    ]

.. option:: to_callow

``to_callow`` is similar to ``to_allow`` but with exception that
provided keys are case sensitive. Regex pattern is also supported.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        to_callow=['.eu']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_image_list))

.. code-block:: python

    [
        'http://demo.com',
        'http://demo.net'
    ]

Lets recreate same example as before but with a uppercase key.

.. code-block:: python

    test_list = ['http://demo.com', 'http://demo.net', 'http://demo.eu']

    list_parser = ed.List(
        parser=ed.Url(),
        to_callow=['.EU']
    )

Now lets parse ``test_list`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_list))

.. code-block:: python

    [
        'http://demo.com',
        'http://demo.net',
        'http://demo.eu'
    ]

.. option:: multiply_keys

Setting values into ``multiply_keys`` enables you to parse ``str`` or a first
value from a ``list`` into multiple values. Lets check bellow example for a
better understanding.

.. code-block:: python

    test_url = 'https://demo.com/imgs/1.jpg'

    list_parser = ed.List(
        parser=ed.Url(),
        multiply_keys=[('1.jpg', ['1.jpg', '2.jpg', '3.jpg', '4.jpg'])]
    )

Now lets parse ``test_url`` data and print our result.

.. code-block:: python

    print(list_parser.parse(test_url))

.. code-block:: python

    [
        'https://demo.com/imgs/1.jpg',
        'https://demo.com/imgs/2.jpg',
        'https://demo.com/imgs/3.jpg',
        'https://demo.com/imgs/4.jpg'
    ]

If instead of

.. code-block:: python

    test_url = 'https://demo.com/imgs/1.jpg'

we would provide

.. code-block:: python

    test_url = ['https://demo.com/imgs/1.jpg']

or

.. code-block:: python

    test_url = ['https://demo.com/imgs/1.jpg', 'https://demo.com/imgs/no-image.jpg']

We would still get same result as in example above.

.. option:: normalize

.. option:: capitalize

.. option:: title

.. option:: uppercase

.. option:: lowercase

.. option:: replace_keys

.. option:: remove_keys

.. option:: split_text_key

.. option:: split_text_keys

.. option:: take

.. option:: skip

.. option:: text_num_to_numeric

.. option:: language

.. option:: fix_spaces

.. option:: escape_new_lines

.. option:: new_line_replacement

.. option:: add_stop

.. option:: deny

.. option:: cdeny


UrlList
=======
.. autoclass:: easydata.parsers.list::UrlList

examples coming soon ...

.. option:: from_text

.. option:: remove_qs

.. option:: qs

.. option:: domain

.. option:: protocol


EmailSearchList
===============
.. autoclass:: easydata.parsers.list::EmailSearchList

``EmailSearchList`` will search for emails in a text (html,xml,json,yaml,etc.) and
return a list of validated email addresses.


examples coming soon ...
