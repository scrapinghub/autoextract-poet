.. _`intro`:

============
Introduction
============

Installing autoextract-poet
===========================

``autoextract-poet`` is a regular PyPI package that can be installed
using ``pip``. But you'll rarely need to do so, because
the most common way to use the definitions from ``autoextract-poet``
is by creating spiders using scrapy-autoextract_.

Visit the scrapy-autoextract_ documentation for its installation
details.

Basic usage in a spider
=======================

The usual way to extract data from a page is by writing a spider with
a ``parse`` method that scrape the data from the page HTML using
``css`` or ``xpath`` selectors. Below you can find a simple example
that extracts data from a `books.toscrape.com <http://books.toscrape.com>`_
page.

.. code-block:: python

    import scrapy

    class ProductSpider(scrapy.Spider):

        name = "products"
        start_urls = ['https://books.toscrape.com/catalogue/sharp-objects_997/index.html']

        def parse(self, response):
            product = {}
            product_sel = response.css("div.product_main")
            product["name"] = product_sel.css("h1 ::text").get()
            product['description'] = response.xpath(
                "//div[@id='product_description']/following-sibling::p/text()"
            ).get()
            # More attributes extracted ...
            yield product

Let's leverage `AutoExtract API`_ to extract the data for us without having
to deal with selectors at all. In the following
spider we have modified the ``parse`` method arguments:
a new argument ``product_page`` of type ``AutoExtractProductPage`` has been included.

.. code-block:: python

    import scrapy
    from autoextract_poet.pages import AutoExtractProductPage
    from scrapy_poet import DummyResponse

    class ProductSpider(scrapy.Spider):

        name = "products"
        start_urls = ['https://books.toscrape.com/catalogue/sharp-objects_997/index.html']

        def parse(self, response: DummyResponse, product_page: AutoExtractProductPage):
            product = product.to_item()
            # product is now an object full of attributes, like name, description, etc
            yield product

`scrapy-poet`_ will automatically perform a request to the API
and will populate ``product_page`` accordingly with the results.
As easy as that.

Many page types are supported: products, articles, job postings, vehicles, real estate,
comments, etc. The full list can be seen `here <https://docs.zyte.com/automatic-extraction.html#result-fields>`_

There is one Page Object class defined for each supported page type.
For example you might include an argument of type ``AutoExtractArticlePage``
in your spider callback to extract the
data from an article page. The full list of available Page Object classes can
be see at the :ref:`Pages` API page.

The former spider won't work as is by default. Some configuration is required.
Please, visit the `scrapy-autoextract configuration page <https://github.com/scrapinghub/scrapy-autoextract#configuration-1>`_
for the details. In this page you can find also the explanation about
why the ``DummyResponse`` type annotation was used.

.. _web-poet: https://github.com/scrapinghub/web-poet
.. _andi: https://github.com/scrapinghub/andi
.. _parsel: https://github.com/scrapinghub/parsel
.. _scrapy-autoextract: https://github.com/scrapinghub/scrapy-autoextract
.. _`AutoExtract API`: https://docs.zyte.com/automatic-extraction.html
.. _`scrapy-poet`: https://scrapy-poet.readthedocs.io/en/stable/