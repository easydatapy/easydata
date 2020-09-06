.. _`parsers-url`:

===========
Url Parsers
===========

Url
===

.. autoclass:: easydata.parsers.url::Url

``Url`` parser is based upon ``Text`` parser and therefore inherits all parameters
from it and it's usage. One differences is that ``normalize`` parameter is set to
``False`` while in ``Text`` parser is set to ``True`` by default.

To read docs regarding other parameters than the one described here, please go to
:ref:`parsers-text` documentation.

Getting Started
---------------

Lets import first ``parsers`` module and ``jp`` instance from ``queries`` module

.. code-block:: python

    >>> from easydata import parsers
    >>> from easydata.queries import jp

``Bool`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'url': 'demo.com/home'}
    >>> parsers.Url(jp('url')).parse(test_dict)
    https://demo.com/home

In this case we see that url in a test_dict is partial. ``Url`` parser will try
to construct and output always full urls.

qs
--

With ``qs`` parameter we can manipulate urls query strings. We can change existing
ones or add new ones.

Lets first try to change existing one.

.. code-block:: python

    >>> test_url = 'https://demo.com/?home=true''
    >>> parsers.Url(qs={'home': 'false'}).parse(test_url)
    'https://demo.com/?home=false'

Now lets try to change existing one and at the same time add a new query
string value.

.. code-block:: python

    >>> test_url = 'https://demo.com/?home=true'
    >>> parsers.Url(qs={'home': 'false', 'country': 'SI'}).parse(test_url)
    'https://demo.com/?home=false&country=SI'


remove_qs
---------

With ``remove_qs`` we can remove query string keys and it's values.

If we provide to ``remove_qs`` a str key, then only a single query string key
and value will be removed as we can see bellow.

.. code-block:: python

    >>> test_url = 'https://demo.com/?home=false&country=SI'
    >>> parsers.Url(remove_qs='home').parse(test_url)
    'https://demo.com/?country=SI'

We can also delete multiple query string keys and it's values at the same time
by providing a ``list`` of ``str`` keys to a ``remove_qs`` parameter.

.. code-block:: python

    >>> test_url = 'https://demo.com/?home=false&country=SI&currency=EUR'
    >>> parsers.Url(remove_qs=['home', 'country']).parse(test_url)
    'https://demo.com/?currency=EUR'

If we set ``remove_qs`` to ``True`` then all query string keys and values
will be removed.

.. code-block:: python

    >>> test_url = 'https://demo.com/?home=false&country=SI'
    >>> parsers.Url(remove_qs=True).parse(test_url)
    'https://demo.com/'

from_text
---------

``Url`` parser has ability to extract url from a text as we can see in example
bellow.

.. code-block:: python

    >>> test_text = 'Home url is:  https://demo.com/home  !!!'
    >>> parsers.Url(from_text=True).parse(test_text)
    'https://demo.com/home'

domain
------

In some cases we can get only partial url links without a domain, especially
when we are scraping websites and for cases like this setting ``domain`` parameter
with a domain name will help with full url link construction.

.. code-block:: python

    >>> test_url = '/product/1122'
    >>> parsers.Url(domain='http://demo.com').parse(test_url)
    'http://demo.com/product/1122'

domain parameter value can also be provided without a protocol like ``http`` or
``https``. If that's the case then a default protocol ``https`` will be used in
order to construct full url.

.. code-block:: python

    >>> test_url = '/product/1122'
    >>> parsers.Url(domain='demo.com').parse(test_url)
    'https://demo.com/product/1122'

protocol
--------

As we saw in example above, default protocol ``https`` is used when provided domain
name in ``domain`` parameter has a missing protocol. We can change our default
protocol value ``https`` by specifying new value into protocol parameter.

.. code-block:: python

    >>> test_url = '/product/1122'
    >>> parsers.Url(domain='demo.com', protocol='ftp').parse(test_url)
    'ftp://demo.com/product/1122'
