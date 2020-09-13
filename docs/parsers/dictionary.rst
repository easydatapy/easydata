.. _`parsers-dictionary`:

==================
Dictionary Parsers
==================

Dict
====
.. autoclass:: easydata.parsers.dict::Dict

examples coming soon ...

.. option:: query

.. option:: key_parser

.. option:: val_parser

.. option:: key_query

.. option:: val_query

.. option:: ignore_non_values

* Default: *False*

Ignore all keys in a ``dict`` that has ``None`` type.

.. option:: ignore_non_keys

* Default: *True*

Ignore all values in a ``dict`` that has ``None`` type.

.. option:: key_normalize

* Default: *True*

When set to ``True``, it will fix bad encoding in dict keys.

.. option:: key_title

* Default: *False*

When set to ``True``, it will convert in a dict key all first chars in a word to uppercase.

.. option:: key_uppercase

* Default: *False*

When set to ``True``, it will convert all chars in a dict keys to uppercase.

.. option:: key_lowercase

* Default: *False*

When set to ``True``, it will convert all chars in a dict keys to lowercase.

.. option:: key_replace_keys

* Default: *None*

We can replace chars/words in a dict keys through ``key_replace_keys`` parameter.
``key_replace_keys`` can accept regex pattern as a lookup key and is not
case sensitive.

.. option:: key_remove_keys

* Default: *None*

We can remove chars/words in a dict keys through ``key_remove_keys`` parameter.
``key_remove_keys`` can accept regex pattern as a lookup key and is not
case sensitive.

.. option:: key_split_text_key

* Default: *None*

Text in a dict key can be split with ``key_split_text_key``. By default split index
is ``0``.

.. option:: key_split_text_keys

* Default: *None*

``key_split_text_keys`` work in a same way as ``key_split_text_key`` but instead
of single split key it accepts list of keys.

.. option:: key_take

* Default: *None*

With ``key_take`` parameter we can limit maximum number of chars in a dict keys.

.. option:: key_skip

* Default: *None*

With ``key_skip`` parameter we can skip defined number of chars from the start in a
dict keys.

.. option:: key_fix_spaces

* Default: *True*

With key_fix_spaces parameter set to True, all multiple spaces between chars will be
removed and left with only single one between chars.

.. option:: key_allow

.. option:: key_callow

.. option:: key_deny

.. option:: key_cdeny


TextDict
========
.. autoclass:: easydata.parsers.dict::TextDict

examples coming soon ...

.. option:: val_normalize

* Default: *True*

When set to ``True``, it will fix bad encoding in dict values.

.. option:: val_title

* Default: *False*

When set to ``True``, it will convert in a dict value all first chars in a word to uppercase.

.. option:: val_uppercase

* Default: *False*

When set to ``True``, it will convert all chars in a dict values to uppercase.

.. option:: val_lowercase

When set to ``True``, it will convert all chars in a dict values to lowercase.

.. option:: val_replace_keys

.. option:: val_remove_keys

.. option:: val_split_text_key

.. option:: val_split_text_keys

.. option:: val_take

.. option:: val_skip

.. option:: val_fix_spaces

.. option:: val_allow

.. option:: val_callow

.. option:: val_deny

.. option:: val_cdeny


BoolDict
========
.. autoclass:: easydata.parsers.dict::BoolDict

examples coming soon ...

.. option:: val_contains

.. option:: val_ccontains

.. option:: val_contains_query

.. option:: val_contains_query_source

.. option:: val_empty_as_false


PriceFloatDict
==============
.. autoclass:: easydata.parsers.dict::PriceFloatDict

examples coming soon ...

.. option:: val_decimals

* Default: *2*

We can manipulate how many ``decimals`` price in a parsed dict values will be have.
By default this limit is ``2``, but we can change this value with a ``val_decimals``
parameter.

.. option:: val_min_value

* Default: *None*

.. option:: val_max_value

* Default: *None*


PriceTextDict
=============
.. autoclass:: easydata.parsers.dict::PriceTextDict

Works exactly the same as ``PriceFloatDict``, but value type is ``str`` instead of ``float``.
