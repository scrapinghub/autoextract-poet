.. _`intro`:

============
Introduction
============

Installing autoextract-poet
===========================

``autoextract-poet`` is a regular PyPI package that can be installed
using ``pip``: ``pip install autoextract-poet``. It is also a dependency
of scrapy-autoextract_, and installed automatically
if you use scrapy-autoextract.

Basic usage
===========

You can use items defined by autoextract-poet just as regular Python objects,
to standardize item definitions. They are implemented as attr.s classes, and
can be used as Scrapy_ items directly, or converted
to dictionaries (e.g. for serialization) via itemadapter_.

scrapy-autoextract_ provides an automatic way to extract items defined
here from any website, using Scrapy_ and `Autoextract API`_.
See its `scrapy-autoextract documentation`_ for more.

.. _scrapy-autoextract documentation: https://github.com/scrapinghub/scrapy-autoextract#the-providers

Compatibility with new fields added to the API
==============================================

Eventually, some new fields could be added to the Autoextract API.
When you're creating ``autoextract-poet`` items from Autoextract responses,
the library would ignore unknown fields by default,
until you upgrade the library to a version containing the new field.
But you might want to keep the unknown (new) fields even if you don't update
the ``autoextract-poet`` library.

If you're using Scrapy_ (or itemadapter_), you can make these unknown
attributes exposed in the output by registering
:class:`~.AutoExtractAdapter` in itemadapter's ADAPTER_CLASSES:

.. code-block:: python

    from autoextract_poet import AutoExtractAdapter
    from itemadapter import ItemAdapter
    ItemAdapter.ADAPTER_CLASSES.appendleft(AutoExtractAdapter)

For example, you can put this code to settings.py of your Scrapy project.

.. _Scrapy: https://github.com/scrapy/scrapy
.. _scrapy-poet: https://scrapy-poet.readthedocs.io/en/stable/
.. _scrapy-autoextract: https://github.com/scrapinghub/scrapy-autoextract
.. _itemadapter: https://github.com/scrapy/itemadapter
.. _`AutoExtract API`: https://docs.zyte.com/automatic-extraction.html
