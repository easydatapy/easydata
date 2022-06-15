.. _`parsers-time`:

============
Time Parsers
============
Time parsers are based upon ``Text`` parser and therefore inherits all parameters
from it and it's usage. One differences is that ``normalize`` parameter is set to
``False`` while in ``Text`` parser is set to ``True`` by default.

To read docs regarding other parameters than the one described here, please go to
:ref:`parsers-text` documentation.


DateTime
========
.. autoclass:: easydata.parsers.time::DateTime

``DateTime`` parser will try to convert date time from a string to our custom
date time format.

Getting Started
---------------
Lets import first ``easydata`` module.

.. code-block:: python

    >>> import easydata as ed

``DateTime`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'datetime': 'Fri, 10 Dec 2018 10:55:50'}
    >>> ed.DateTime(ed.jp('datetime')).parse(test_dict)
    '12/10/2018 10:55:50'

Any invalid string without datetime will cause ``DateTime`` parser to return None.

.. code-block:: python

    >>> test_dict = {'datetime': 'n/a'}
    >>> ed.DateTime(ed.jp('datetime')).parse(test_dict)
    None

Parameters
----------
.. option:: datetime_format

We can change our date time output in any valid str format that we want through a
``datetime_format`` parameter.

.. code-block:: python

    >>> test_date_text = 'Fri, 10 Dec 2018 10:55:50'
    >>> ed.DateTime(datetime_format='%d.%m.%Y %H:%M:%S').parse(test_date_text)
    '10.12.2018 10:55:50'

.. note::

    Default value of *datetime_format* parameter can be defined through a config
    variable :ref:`config-ed-datetime-format` in a config file or a model.

.. option:: min_year

If we set value in a ``min_year`` parameter and year of our date time in a string is
bellow our min year limit, then the output will be ``None``.

Lets try first with a valid year.

.. code-block:: python

    >>> test_date_text = 'Fri, 10 Dec 2018 10:55:50'
    >>> ed.DateTime(min_year='2015').parse(test_date_text)
    '12/10/2018 10:55:50'

Now with a year that it's bellow our ``min_year`` limit.

.. code-block:: python

    >>> test_date_text = 'Fri, 10 Dec 2010 10:55:50'
    >>> ed.DateTime(min_year='2015').parse(test_date_text)
    None

.. option:: max_year

If we set value in a ``max_year`` parameter and year of our date time in a string is
over our max year limit, then the output will be ``None``.

Lets try first with a valid year.

.. code-block:: python

    >>> test_date_text = 'Fri, 10 Dec 2018 10:55:50'
    >>> ed.DateTime(max_year='2020').parse(test_date_text)
    '12/10/2018 10:55:50'

Now with a year that it's over our ``max_year`` limit.

.. code-block:: python

    >>> test_date_text = 'Fri, 10 Dec 2022 10:55:50'
    >>> ed.DateTime(max_year='2020').parse(test_date_text)
    None


DateTimeSearch
==============
.. autoclass:: easydata.parsers.time::DateTimeSearch

``DateTimeSearch`` works exactly the same as ``DateTime`` parser with a difference
that can extract date time from sentences that have other content besides date time.

Lets try first to extract date from a sentence with a ``DateTime`` parser.

As we can see ... ordinary

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.DateTime().parse(test_text)
    None

As we can see ... ordinary ``DateTime`` parser cannot handle text if there is some
other text besides date time and in situations like this ``DateTimeSearch`` parser
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.DateTimeSearch().parse(test_text)
    '12/10/2018 10:55:50'

Date
====
.. autoclass:: easydata.parsers.time::Date

``Date`` parser works exactly the same as ``DateTime`` parser but it's output is only
date and it's has it's own ``date_format`` parameter to format date output.

Getting Started
---------------
Lets import first ``easydata`` module.

.. code-block:: python

    >>> import easydata as ed

``Date`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'datetime': 'Fri, 10 Dec 2018 10:55:50'}
    >>> ed.Date(ed.jp('datetime')).parse(test_dict)
    '12/10/2018'

Any invalid string without a date will cause ``Date`` parser to return None.

.. code-block:: python

    >>> test_dict = {'date': 'n/a'}
    >>> ed.DateTime(ed.jp('date')).parse(test_dict)
    None

Parameters
----------
.. option:: date_format

We can change our date time output in any valid str format that we want through a
``date_format`` parameter.

.. code-block:: python

    >>> test_date_text = 'Fri, 10 Dec 2018 10:55:50'
    >>> ed.DateTime(date_format='%d.%m.%Y').parse(test_date_text)
    '10.12.2018'

.. note::

    Default value of *date_format* parameter can be defined through a config
    variable :ref:`config-ed-date-format` in a config file or a model.


DateSearch
==========
.. autoclass:: easydata.parsers.time::DateSearch

``DateSearch`` works exactly the same as ``Date`` parser with a difference
that can extract date from sentences that have other content besides date.

Lets try first to extract date from a sentence with a ``Date`` parser.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Date().transform(test_text)
    None

As we can see ... ordinary

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Date().transform(test_text)
    None

As we can see ... ordinary

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Date().parse(test_text)
    None

As we can see ... ordinary ``Date`` parser cannot handle text if there is some
other text besides date and in situations like this ``DateSearch`` parser
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.DateSearch().transform(test_text)
    '12/10/2018'
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.DateSearch().transform(test_text)
    '12/10/2018'
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.DateSearch().parse(test_text)
    '12/10/2018'


Time
====
.. autoclass:: easydata.parsers.time::Time

``Time`` parser works exactly the same as ``DateTime`` parser but it's output is only
time and it's has it's own ``time_format`` parameter to format time output.

Getting Started
---------------
Lets import first ``easydata`` module.

.. code-block:: python

    >>> import easydata as ed

``Time`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'datetime': 'Fri, 10 Dec 2018 10:55:50'}
    >>> ed.Time(ed.jp('datetime')).parse(test_dict)
    '10:55:50'

Any invalid string without a date will cause ``Time`` parser to return None.

.. code-block:: python

    >>> test_dict = {'time': 'n/a'}
    >>> ed.Time(ed.jp('time')).parse(test_dict)
    None

Parameters
----------
.. option:: time_format

We can change our date time output in any valid str format that we want through a
``time_format`` parameter.

.. code-block:: python

    >>> test_date_text = 'Fri, 10 Dec 2018 10:55:50'
    >>> ed.Time(time_format='%H-%M-%S').parse(test_date_text)
    '10-55-50'

.. note::

    Default value of *time_format* parameter can be defined through a config
    variable :ref:`config-ed-time-format` in a config file or a model.


TimeSearch
==========
.. autoclass:: easydata.parsers.time::TimeSearch

``TimeSearch`` works exactly the same as ``Time`` parser with a difference
that can extract time from sentences that have other content besides time.

Lets try first to extract date from a sentence with a ``Time`` parser.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Time().transform(test_text)
    None

As we can see ... ordinary

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Time().transform(test_text)
    None

As we can see ... ordinary

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Time().parse(test_text)
    None

As we can see ... ordinary ``Time`` parser cannot handle text if there is some
other text besides date and in situations like this ``TimeSearch`` parser
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.TimeSearch().transform(test_text)
    '10:55:50'
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.TimeSearch().transform(test_text)
    '10:55:50'
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.TimeSearch().parse(test_text)
    '10:55:50'


Year
====
.. autoclass:: easydata.parsers.time::Year

``Year`` parser works exactly the same as ``DateTime`` parser but it's output is only
year.

Getting Started
---------------
Lets import first ``easydata`` module.

.. code-block:: python

    >>> import easydata as ed

``Year`` supports any query object for fetching data.

.. code-block:: python

    >>> test_dict = {'datetime': 'Fri, 10 Dec 2018 10:55:50'}
    >>> ed.Year(ed.jp('datetime')).parse(test_dict)
    '2018'

Any invalid string without a date will cause ``Year`` parser to return None.

.. code-block:: python

    >>> test_dict = {'date': 'n/a'}
    >>> ed.Year(ed.jp('date')).parse(test_dict)
    None


YearSearch
==========
.. autoclass:: easydata.parsers.time::YearSearch

``YearSearch`` works exactly the same as ``Year`` parser with a difference
that can extract time from sentences that have other content besides date.

Lets try first to extract date from a sentence with a ``Year`` parser.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Year().transform(test_text)
    None

As we can see ... ordinary

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Year().transform(test_text)
    None

As we can see ... ordinary

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.Year().parse(test_text)
    None

As we can see ... ordinary ``Year`` parser cannot handle text if there is some
other text besides date and in situations like this ``YearSearch`` parser
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.YearSearch().transform(test_text)
    '2018'
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.YearSearch().transform(test_text)
    '2018'
will work.

    >>> test_text = 'It has happened on 10 Dec 2018 at 10:55:50'
    >>> ed.YearSearch().parse(test_text)
    '2018'
