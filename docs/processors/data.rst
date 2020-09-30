.. _`processors-data`:

===============
Data Processors
===============

.. _processors-data-processor:

DataProcessor
=============
.. autoclass:: easydata.processors.data::DataProcessor

``DataProcessor`` directly extends ``DataBaseProcessor`` and it's default parameters.
On it's own, it doesn't add any new functionalities besides those that are inherited
from a ``DataBaseProcessor``.

.. note::

    All other data processors are based on ``DataBaseProcessor`` and if you are
    creating your own, then you should also extend from ``DataBaseProcessor``.
    Also ``DataBaseProcessor`` cannot be used in a model, since it's an abstract
    class.

Parameters
----------
.. option:: source

Default value of ``source`` parameter is ``data``. This means that by default
``DataProcessor`` will always look into ``DataBag`` for a ``data`` key and
it's content. If we need to modify content from a different ``source``
in a ``DataBag``, then we just need to change ``source`` value.

.. option:: new_source

By default content that is getting processed from the ``source`` value, will be
overwritten in a ``DataBag`` under key that is specified by ``source`` parameter.

We can still preserve original content in a ``DataBag``, by specifying new source
name under a ``new_source`` parameter.

.. note::

    If we store modified content under a new key in a **DataBag**, parsers by
    default will look into a **data** key source and we need to specify that
    under a parsers parameter **source**, which name is same as key from a
    ``new_source`` in a data processor property.

.. option:: process_source_data


.. _processors-data-to-pq-processor:

DataToPqProcessor
=================
.. autoclass:: easydata.processors.data::DataToPqProcessor


.. _processors-data-json-to-dict-processor:

DataJsonToDictProcessor
=======================
.. autoclass:: easydata.processors.data::DataJsonToDictProcessor


.. _processors-data-yaml-to-dict-processor:

DataYamlToDictProcessor
=======================
.. autoclass:: easydata.processors.data::DataYamlToDictProcessor


.. _processors-data-json-from-query-to-dict-processor:

DataJsonFromQueryToDictProcessor
================================
.. autoclass:: easydata.processors.data::DataJsonFromQueryToDictProcessor


.. _processors-data-xml-to-dict-processor:

DataXmlToDictProcessor
======================
.. autoclass:: easydata.processors.data::DataXmlToDictProcessor


.. _processors-data-text-from-re-processor:

DataTextFromReProcessor
=======================
.. autoclass:: easydata.processors.data::DataTextFromReProcessor


.. _processors-data-json-from-re-to-dict-processor:

DataJsonFromReToDictProcessor
=============================
.. autoclass:: easydata.processors.data::DataJsonFromReToDictProcessor


.. _processors-data-from-query-processor:

DataFromQueryProcessor
======================
.. autoclass:: easydata.processors.data::DataFromQueryProcessor


.. _processors-data-variants-processor:

DataVariantsProcessor
=====================
.. autoclass:: easydata.processors.data::DataVariantsProcessor
