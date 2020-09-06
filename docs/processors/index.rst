==========
Processors
==========

* :ref:`processors-data` - are extensions to models which help to prepare/convert data for
  parser in cases data is more complex and with regular query selectors it cannot be selected
  in it’s raw form.

* :ref:`processors-item` - similar to data processor but instead of transforming data for a
  parser, their purpose is to modify already parsed item dictionary.

.. note::

    The greatest power of processor usage is to extend or create it from scratch in order
    to handle scenarios that are not covered by default processors. Custom processors can
    be easily reused between different models when needed.

.. toctree::
    :maxdepth: 2
    :hidden:

    data
    item
