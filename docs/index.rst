Welcome to easydata's documentation!
====================================
.. warning::

    EasyData is in early stages of development; backwards incompatible
    changes are possible without deprecation warnings until beta status
    is reached and therefore is not suitable to be used in production.


What is EasyData
================
``EasyData`` is data object pattern that provides transformation of item data
from various sources (text, html, xml, json, dictionaries, lists and others) to a
python dictionary with option to even combine different types of sources in order
to transform to dictionary.

It uses component based mapping at the hearth and it's concept is similar to ORM-like
models.

**The benefits of using EasyData are:**

* focusing on the object-oriented business logic
* uniform extraction logic between various sources
* speeds up development process of creating a transformer/parser significantly
* time reduction regarding maintenance since it offers clear readability and
  clarity regarding what each components does.
* extraction and parsing logic re-usability
* high and low level option for parsing so that we don't hit any limitations
* option to create custom components for specific needs if needed
* defaults can be changed through configuration on various levels
* creating test cases is a breeze since each component was created to be
  used independently if needed.

.. note::

    EasyData is not tied to any framework, nor it's a framework and it can be
    easily added to existing projects.

**Applications:**

* Web scraping. It can easily be integrated with scrapy or any other python
  based solution or even your own.
* Transforming API and FEED data from various formats.
* Transforming/preparing data for API or FEED
* Transforming/preparing data for a database.

**It does not:**

* make requests.*
* perform database operation.*
* make validation of item dictionary.*
* read feed files or process multiple items at the same time since it's architecture
  is designed to process each row/item at the time.*


How to read documentation?
==========================
Documentation is divided into chapters which are marked with numbers and is best to
follow it in that order, if you are familiarizing with the package for the first time.


Where next?
===========
If you are new to EasyData, please refer to :ref:`getting-started` section where you
will get to know basics, and if you are already familiar with basics, then jump to
:ref:`advanced` section.


Contributing
============
**Yes please!**  We are always looking for contributions, additions and improvements.

The source is available on `GitHub <http://github.com/easydatapy/easydata>`_
and contributions are always encouraged. Contributions can be as simple as
minor tweaks to this documentation or the core.

.. toctree::
    :maxdepth: 1
    :numbered: 3
    :hidden:

    installation
    getting_started
    architecture
    advanced
    scrapy
    requests
    config
    parsers/index
    queries/index
    processors/index
    extending/index
    faq
    contributing
