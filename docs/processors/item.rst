.. _`processors-item`:

===============
Item Processors
===============

.. _processors-item-keys-merge-into-list-processor:


ItemKeysMergeIntoListProcessor
==============================
.. autoclass:: easydata.processors.item::ItemKeysMergeIntoListProcessor

``ItemKeysMergeIntoDictProcessor`` creates a list of values under a new key on
a basis of specified keys in item dictionary.

Parameters
----------

.. option:: new_item_key

.. option:: item_keys

.. option:: preserve_original

.. option:: ignore_none


.. _processors-item-keys-merge-processor:

ItemKeysMergeProcessor
======================
.. autoclass:: easydata.processors.item::ItemKeysMergeProcessor

Parameters
----------

.. option:: new_item_key

.. option:: preserve_original

.. option:: separator


.. _processors-item-keys-merge-into-dict-processor:

ItemKeysMergeIntoDictProcessor
==============================
.. autoclass:: easydata.processors.item::ItemKeysMergeIntoDictProcessor

``ItemKeysMergeIntoDictProcessor`` creates a dictionary under a new key on
a basis of specified keys in item dictionary.

Parameters
----------

.. option:: new_item_key

.. option:: item_keys

.. option:: preserve_original

.. option:: ignore_none


.. _processors-item-value-to-str-processor:

ItemValueToStrProcessor
=======================
.. autoclass:: easydata.processors.item::ItemValueToStrProcessor

``ItemValueToStrProcessor`` converts values from various types to str.

Parameters
----------

.. option:: item_keys

.. option:: none_as_empty_string


.. _processors-item-remove-keys-processor:

ItemRemoveKeysProcessor
=======================
.. autoclass:: easydata.processors.item::ItemRemoveKeysProcessor

``ItemRemoveKeysProcessor`` removes keys from item dictionary.

Parameters
----------

.. option:: item_keys


.. _processors-item-discount-processor:

ItemDiscountProcessor
=====================
.. autoclass:: easydata.processors.item::ItemDiscountProcessor

``ItemDiscountProcessor`` looks for parsed ``price`` and ``sale_price`` in item
dictionary and calculates discount percentage between those two values. Finally
it creates a new discount key in item dictionary and attaches discount value to it.
If our price and sale price values live under different keys under item dictionary
than default ones ``price`` and ``sale_price``, then we can through parameters,
change those default values in order to suit our needs.

All parameters that ``ItemDiscountProcessor`` accepts are listed bellow:

Parameters
----------

.. option:: item_price_key

.. note::

    Default value of *item_price_key* parameter can be defined through a config variable
    :ref:`config-ed-item-discount-item-price-key` in a config file or a model.

.. option:: item_sale_price_key

.. note::

    Default value of *item_sale_price_key* parameter can be defined through a config variable
    :ref:`config-ed-item-discount-item-sale-price-key` in a config file or a model.

.. option:: item_discount_key

.. note::

    Default value of *item_discount_key* parameter can be defined through a config variable
    :ref:`config-ed-item-discount-item-discount-key` in a config file or a model.

.. option:: decimals

.. note::

    Default value of *decimals* parameter can be defined through a config variable
    :ref:`config-ed-item-discount-decimals` in a config file or a model.

.. option:: no_decimals

.. note::

    Default value of *no_decimals* parameter can be defined through a config variable
    :ref:`config-ed-item-discount-no-decimals` in a config file or a model.

.. option:: remove_item_sale_price_key

.. note::

    Default value of *remove_item_sale_price_key* parameter can be defined through a config
    variable :ref:`config-ed-item-discount-rm-item-sale-price-key` in a config file or a model.
