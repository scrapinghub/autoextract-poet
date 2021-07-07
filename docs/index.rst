==============================
autoextract-poet documentation
==============================

``autoextract-poet`` contains the the Page Objects definitions required
to extract data using Zyte `AutoExtract API`_ in combination with
`scrapy-poet`_ and `scrapy-autoextract`_.

The `AutoExtract API`_ is able to convert pages into data automatically.
It support multiple types of pages, like articles, products, real estate,
comments, job posting, reviews, etc. See the full list of supported
page types `here <https://docs.zyte.com/automatic-extraction.html#result-fields>`_.

See also `web-poet`_  for an introduction about the Page Objects
paradigm and the `scrapy-poet tutorial`_ for an introduction
about how to use Page Objects with Scrapy spiders.

:ref:`license` is BSD 3-clause.

.. _`AutoExtract`: https://www.zyte.com/data-extraction/
.. _`web-poet`: https://github.com/scrapinghub/web-poet
.. _docs: https://web-poet.readthedocs.io/en/stable/
.. _`scrapy-poet`: https://scrapy-poet.readthedocs.io/en/stable/
.. _`AutoExtract API`: https://docs.zyte.com/automatic-extraction.html
.. _`zyte-autoextract`: https://github.com/zytedata/zyte-autoextract
.. _`scrapy-autoextract`: https://github.com/scrapinghub/scrapy-autoextract
.. _`scrapy-poet tutorial`: https://scrapy-poet.readthedocs.io/en/stable/intro/tutorial.html

.. toctree::
   :caption: Getting started
   :maxdepth: 1

   intro.rst
   enrich.rst

.. toctree::
   :caption: Documentation
   :maxdepth: 1

   api_reference
   contributing
   changelog
   license
