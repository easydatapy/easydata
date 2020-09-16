.. _`parsers-email`:

=============
Email Parsers
=============

Email
=====
.. autoclass:: easydata.parsers.email::Email

``Email`` is a parser which will extract email address from a text and if not valid,
it will return ``None``.

Getting Started
---------------
Lets try to parser various text samples and see the results.

.. code-block:: python

    >>> parsers.Email().parse("easydatapy@gmail.com")
    'easydatapy@gmail.com'

    >>> parsers.Email().parse("easy.datapy@gmail.co.uk")
    'easy.datapy@gmail.co.uk'

    >>> parsers.Email().parse("Contact please easydatapy@gmail.com!!!")
    'easydatapy@gmail.com'

    >>> parsers.Email().parse("easy.datapy@gmail.com")
    'easy.datapy@gmail.com'

    >>> parsers.Email().parse("Various chars 1ea-12sy.da_ta4.py99@gmail.com :)")
    '1ea-12sy.da_ta4.py99@gmail.com'

    >>> parsers.Email().parse('<input value="easydatapy@gmail.com">')
    'easydatapy@gmail.com'

    >>> parsers.Email().parse('<a href="mailto:easydatapy@gmail.com">Here</a>')
    'easydatapy@gmail.com'

    >>> parsers.Email().parse("Uppercase works also EASYdatapy@GMAIL.COM")
    'EASYdatapy@GMAIL.COM'

    >>> parsers.Email(lowercase=True).parse("Will become lowercase EASYdatapy@GMAIL.COM")
    'easydatapy@gmail.com'

Lets try to parse some invalid emails and see what happens.

.. code-block:: python

    >>> parsers.Email().parse("easydatapy@gmail")
    None

    >>> parsers.Email().parse("easydatapy@")
    None

    >>> parsers.Email().parse("@gmail.com")
    None

Parameters
----------
.. option:: domain

If domain parameter added, then it's value will be added to an email address if it's missing
domain name.

Lets try to parser various samples and see the results.

.. code-block:: python

    >>> parsers.Email(domain="gmail.com").parse("easydatapy")
    'easydatapy@gmail.com'

    >>> parsers.Email(domain="gmail.com").parse("easydatapy@")
    'easydatapy@gmail.com'

    >>> parsers.Email(domain="gmail.com").parse("Contact please easydatapy@")
    'easydatapy@gmail.com'

    >>> parsers.Email(domain="gmail.com").parse("Contact please easydatapy@ !!")
    None
