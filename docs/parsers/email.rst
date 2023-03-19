.. _`parsers-email`:

=====
Email
=====

Email
=====
.. autoclass:: easydata.parsers.email::Email

``Email`` is a parser which will extract email address from a text and if not valid,
it will return ``None``.

Getting Started
---------------
Lets try to parser various text samples and see the results.

.. code-block:: python

    >>> import easydata as ed

    >>> ed.Email().parse("easydatapy@gmail.com")
    'easydatapy@gmail.com'

    >>> ed.Email().parse("easy.datapy@gmail.co.uk")
    'easy.datapy@gmail.co.uk'

    >>> ed.Email().parse("Contact please easydatapy@gmail.com!!!")
    'easydatapy@gmail.com'

    >>> ed.Email().parse("easy.datapy@gmail.com")
    'easy.datapy@gmail.com'

    >>> ed.Email().parse("Various chars 1ea-12sy.da_ta4.py99@gmail.com :)")
    '1ea-12sy.da_ta4.py99@gmail.com'

    >>> ed.Email().parse('<input value="easydatapy@gmail.com">')
    'easydatapy@gmail.com'

    >>> ed.Email().parse('<a href="mailto:easydatapy@gmail.com">Here</a>')
    'easydatapy@gmail.com'

    >>> ed.Email().parse("Uppercase works also EASYdatapy@GMAIL.COM")
    'EASYdatapy@GMAIL.COM'

    >>> ed.Email(lowercase=True).parse("Will become lowercase EASYdatapy@GMAIL.COM")
    'easydatapy@gmail.com'

Lets try to parse some invalid emails and see what happens.

.. code-block:: python

    >>> ed.Email().parse("easydatapy@gmail")
    None

    >>> ed.Email().parse("easydatapy@")
    None

    >>> ed.Email().parse("@gmail.com")
    None

Parameters
----------
.. option:: domain

If domain parameter added, then it's value will be added to an email address if it's missing
domain name.

Lets try to parser various samples and see the results.

.. code-block:: python

    >>> ed.Email(domain="gmail.com").parse("easydatapy")
    'easydatapy@gmail.com'

    >>> ed.Email(domain="gmail.com").parse("easydatapy@")
    'easydatapy@gmail.com'

    >>> ed.Email(domain="gmail.com").parse("Contact please easydatapy@")
    'easydatapy@gmail.com'

    >>> ed.Email(domain="gmail.com").parse("Contact please easydatapy@ !!")
    None
