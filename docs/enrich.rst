.. _`enrich`:

==================
Enriching the data
==================

It might happen than the data returned by `AutoExtract API`_ is not
enough: some additional information is required. It is possible
to use regular selectors to enrich or amend the data provided by the
API.

Here we present an example of an spider that adds the UPC code to
the extracted product.

.. code-block:: python

    import scrapy
    from autoextract_poet.pages import AutoExtractProductPage

    class ProductSpider(scrapy.Spider):

        name = "products"
        start_urls = ['https://books.toscrape.com/catalogue/sharp-objects_997/index.html']

        def parse(self, response, product_page: AutoExtractProductPage):
            product = product.to_item()
            product._additional_attrs["UPC"] = response.css("tr:nth-child(1) td::text").get()
            yield product

Two things to comment in regards to this example:

* The HTLM from the Scrapy response was used to extract the UPC. This means that
  two requests were made to extract this product: one to the page itself using
  Scrapy to obtain the response (HTML), and one to the AutoExtract API to extract
  the product data.

* The ``_additional_attrs`` dictionary is used to include additional attributes
  not already defined in the :py:class:`autoextract-poet.items.Product`. It is an
  easy way to add new attributes. We'll see later that using a custom pipeline
  is required for this additional attributes to be included in the output
  product.

Using Scrapy to get the HTML from the page might not be the best idea. First,
two different requests are done to fetch the data from the page, so they might
be working with two incoherent versions of the page. Second, rendering the page
in a browser is sometimes required to get the proper HTML. The API is doing so, but
Scrapy isn't.

This is why we recommend to use the HTML returned by the API instead. This ensures that:

* a single request is done: the one to the API
* the returned HTML is exactly the same used by the API to extract the data.
  This ensures the coherence in the resultant product

Below is the updated example using `AutoExtract API HTML <https://docs.zyte.com/automatic-extraction.html#full-html>`_
instead of the Scrapy response:

.. code-block:: python

    import scrapy
    from autoextract_poet.pages import AutoExtractProductPage, AutoExtractWebPage
    from scrapy_poet import DummyResponse

    class ProductSpider(scrapy.Spider):

        name = "products"
        start_urls = ['https://books.toscrape.com/catalogue/sharp-objects_997/index.html']

        def parse(self,
                  response: DummyReponse,
                  product_page: AutoExtractProductPage,
                  html: AutoExtractWebPage):
            product = product.to_item()
            product._additional_attrs["UPC"] = html.css("tr:nth-child(1) td::text").get()
            yield product

The HTML from AutoExtract is now accessible in the callback through the html
argument. Note that we used the ``DummyResponse`` to avoid issuing the Scrapy request.

Pipeline for additional attributes
----------------------------------

Additional attributes added using the facility ``_additional_attrs`` won't
be present in the output of the spider, unless the following pipeline is
included in your Scrapy project:

.. code-block:: python

    from autoextract_poet import AutoExtractAdapter
    from itemadapter import ItemAdapter


    class RemoveEmptyAttrFieldsPipeline:
        def open_spider(self, spider):
            # Serialization for autoextract-poet items
            ItemAdapter.ADAPTER_CLASSES.appendleft(AutoExtractAdapter)

        def process_item(self, item, spider):
            return ItemAdapter(item).asdict()

        def close_spider(self, spider):
            ItemAdapter.ADAPTER_CLASSES.remove(AutoExtractAdapter)

The :py:class:`autoextract-poet.adapters.AutoExtractAdapter` is responsible
for ensuring that all the attributes in ``_additional_attrs`` are also present
in the resultant item.

.. _web-poet: https://github.com/scrapinghub/web-poet
.. _andi: https://github.com/scrapinghub/andi
.. _parsel: https://github.com/scrapinghub/parsel
.. _scrapy-autoextract: https://github.com/scrapinghub/scrapy-autoextract
.. _`AutoExtract API`: https://docs.zyte.com/automatic-extraction.html
.. _`scrapy-poet`: https://scrapy-poet.readthedocs.io/en/stable/