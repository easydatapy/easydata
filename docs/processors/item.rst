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

.. _processors-item-keys-merge-processor:

ItemKeysMergeProcessor
======================

.. autoclass:: easydata.processors.item::ItemKeysMergeProcessor

.. _processors-item-keys-merge-into-dict-processor:

ItemKeysMergeIntoDictProcessor
==============================

.. autoclass:: easydata.processors.item::ItemKeysMergeIntoDictProcessor

``ItemKeysMergeIntoDictProcessor`` creates a dictionary under a new key on
a basis of specified keys in item dictionary.

.. _processors-item-value-to-str-processor:

ItemValueToStrProcessor
=======================

.. autoclass:: easydata.processors.item::ItemValueToStrProcessor

``ItemValueToStrProcessor`` converts values from various types to str.

.. _processors-item-remove-keys-processor:

ItemRemoveKeysProcessor
=======================

.. autoclass:: easydata.processors.item::ItemRemoveKeysProcessor

``ItemRemoveKeysProcessor`` removes keys from item dictionary.

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

item_price_key
--------------

item_sale_price_key
-------------------

item_discount_key
-----------------

decimals
--------

no_decimals
-----------

rm_item_sale_price_key
----------------------
