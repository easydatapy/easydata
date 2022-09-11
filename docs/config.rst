.. _`config`:

======
Config
======
The EasyData config allows you to customize the behaviour of all EasyData components,
including the parsers, processors and models themselves.

The infrastructure of the config provides a global namespace of key-value mappings
that the code can use to pull configuration values from. The config attributes can be
populated through different mechanisms, which are described below.

For a list of available built-in config variables see: :ref:`config-reference`.


Populating config
=================
The Config can be populated using different mechanisms, each of which having a different
precedence. Here is a list of them in decreasing order of precedence:

* Config per model (highest precedence)
* Project config module
* Default global settings (least precedence)

These mechanisms are described in more detail below.

.. note::

    All custom config variables must start with ``ED_``, otherwise they wont be
    recognized by the config loader.

Config per model
----------------
Models can define it's own config attributes that will take precedence and override the
project or global one. They can do so by defining the config key and value through a class
attribute:

.. code-block:: python

    class ProductItemModel(ItemModel):
        ED_LANGUAGE = 'fr'

        ED_DATETIME_FORMAT = ''%d.%m.%Y %H:%M:%S'
        ...

.. _config-project-config-module:

Project config module
---------------------
Global config can be overridden by creating your own config module. Then you need to
tell path to your config module by using an environment variable, ``ED_CONFIG_PATH``.

The value of ``ED_CONFIG_PATH`` should be in Python path syntax, e.g. ``myproject.config``.
Note that the config module should be on the Python
`import search path <https://docs.python.org/3/tutorial/modules.html#tut-searchpath>`_.

.. note::

    The design decision that all config variables start with ``ED_`` is due to possibility
    to use config or settings module from a different framework, e.g. ``scrapy``
    and to prevent any name conflicts.

Default global config
---------------------
The global defaults are located in the ``easydata.config.default`` module and
documented in the :ref:`config-reference` section.


Rationale for config names
==========================
Config names are usually prefixed with the component that they configure. For
example, proper config names for a date time parsers would be ``ED_URL_DOMAIN``,
``ED_URL_PROTOCOL``, etc.


Accessing config
================
Via ``easydata.utils.config``:

.. code-block:: python

    from easydata.utils import config

.. code-block:: python

    >>> config.get('ED_LANGUAGE')
    'en'

Examples above will return default config values or if they are overwritten or newly added
via :ref:`config-project-config-module`

Or via ``config`` property in a ``parser``, ``model`` or ``processor`` components.
Through the ``config`` property in a component, we will get any config value that was defined or
overwritten in a ``model``.

.. _config-reference:


Built-in config reference
=========================
Here's a list of all available ``EasyData`` config names, along with their default values
and the scope where they apply.

The scope, where available, shows where the config is being used and if it's tied
to any particular component. In that case the module of that component will be
shown, typically a parser or a processor. It also means that the component must
be used in order for the config to have any effect.

Default config variables:
-------------------------
.. _config-ed-language:

ED_LANGUAGE
###########
Default: ``'en'``

.. _config-ed-datetime-format:

ED_DATETIME_FORMAT
##################
Default: ``'%m/%d/%Y %H:%M:%S'``

.. _config-ed-date-format:

ED_DATE_FORMAT
##############
Default: ``'%m/%d/%Y'``

.. _config-ed-time-format:

ED_TIME_FORMAT
##############
Default: ``'%H:%M:%S'``

.. _config-ed-datetime-formats:

ED_DATETIME_FORMATS
###################
Default: ``None``

.. _config-ed-datetime-language:

ED_DATETIME_LANGUAGE
####################
Default: ``None``

.. _config-ed-datetime-locales:

ED_DATETIME_LOCALES
###################
Default: ``None``

.. _config-ed-datetime-region:

ED_DATETIME_REGION
##################
Default: ``None``

.. _config-ed-url-domain:

ED_URL_DOMAIN
#############
Default: ``None``

.. _config-ed-url-protocol:

ED_URL_PROTOCOL
###############
Default: ``'https'``

.. _config-ed-price-decimals:

ED_PRICE_DECIMALS
#################
Default: ``2``

.. _config-ed-item-discount-item-price-key:

ED_ITEM_DISCOUNT_ITEM_PRICE_KEY
###############################
Default: ``'price'``

.. _config-ed-item-discount-item-sale-price-key:

ED_ITEM_DISCOUNT_ITEM_SALE_PRICE_KEY
####################################
Default: ``'sale_price'``

.. _config-ed-item-discount-item-discount-key:

ED_ITEM_DISCOUNT_ITEM_DISCOUNT_KEY
##################################
Default: ``'discount'``

.. _config-ed-item-discount-decimals:

ED_ITEM_DISCOUNT_DECIMALS
#########################
Default: ``2``

.. _config-ed-item-discount-no-decimals:

ED_ITEM_DISCOUNT_NO_DECIMALS
############################
Default: ``False``

.. _config-ed-item-discount-rm-item-sale-price-key:

ED_ITEM_DISCOUNT_REMOVE_ITEM_SALE_PRICE_KEY
###########################################
Default: ``False``

.. _config-ed-data-variants-name:

ED_DATA_VARIANTS_NAME
#####################
Default: ``variants``

.. _config-ed-data-variants-key-name:

ED_DATA_VARIANTS_KEY_NAME
#########################
Default: ``variants_key``

.. _config-ed-data-variant-name:

ED_DATA_VARIANT_NAME
####################
Default: ``variant``
