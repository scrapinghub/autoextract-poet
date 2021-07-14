.. _`enrich`:

==================
Enriching the data
==================

It might happen than the data returned by `AutoExtract API`_ is not
enough: some additional information might be required. It is possible
to use regular selectors to enrich or amend the data provided by the
API.

Here we present an example of an spider that adds the UPC code to
the extracted product.

.. code-block:: python

    from typing import Optional
    import scrapy
    from autoextract_poet.pages import AutoExtractProductPage
    from autoextract_poet.items import Product
    import attr

    @attr.s(auto_attribs=True, slots=True)
    class UPCProduct(Product):
        """A product that also has a UPC field"""
        upc: Optional[str] = None

    class ProductSpider(scrapy.Spider):

        name = "products"
        start_urls = ['https://books.toscrape.com/catalogue/sharp-objects_997/index.html']

        def parse(self, response, product_page: AutoExtractProductPage):
            product = product_page.to_item()
            my_product = UPCProduct.from_dict(attr.asdict(product))  # Copying the product
            my_product.upc = response.css("tr:nth-child(1) td::text").get()
            yield my_product

Two things to comment in regards to this example:

* We had to create a new instance of type ``UPCProduct`` and it was initialized
  using the data from the regular ``Product`` instance.

* The HTML from the Scrapy response was used to extract the UPC. This means that
  two requests were made to extract this product: one to the page itself using
  Scrapy to obtain the response (HTML), and one to the AutoExtract API to extract
  the product data.


Using Scrapy to get the HTML from the page might not be the best idea. First,
two different requests are done to fetch the data from the page, so they might
be working with two incoherent versions of the page. Second, rendering the page
in a browser is sometimes required to get the HTML with the desired content.
The API HTML is from the browser, but Scrapy's one isn't.

This is why we recommend to use the HTML returned by the API instead. This ensures that:

* a single request is done: one to the API
* the returned HTML is exactly the same one used by the API to extract the data.
  This ensures the coherence in the resultant product

Below is the updated example using `AutoExtract API HTML <https://docs.zyte.com/automatic-extraction.html#full-html>`_
instead of the Scrapy response:

.. code-block:: python

    from typing import Optional
    import scrapy
    from autoextract_poet.pages import AutoExtractProductPage, AutoExtractWebPage
    from autoextract_poet.items import Product
    from scrapy_poet import DummyResponse
    import attr


    @attr.s(auto_attribs=True, slots=True)
    class UPCProduct(Product):
        """A product that also has a UPC field"""
        upc: Optional[str] = None


    class ProductSpider(scrapy.Spider):

        name = "products"
        start_urls = ['https://books.toscrape.com/catalogue/sharp-objects_997/index.html']

        def parse(self,
                  response: DummyReponse,
                  product_page: AutoExtractProductPage,
                  html: AutoExtractWebPage):
            product = product_page.to_item()
            my_product = UPCProduct.from_dict(attr.asdict(product))
            my_product.upc = html.css("tr:nth-child(1) td::text").get()
            yield my_product

The HTML from AutoExtract is now accessible in the callback through the html
argument. Note that we used the ``DummyResponse`` to avoid issuing the Scrapy request.

It is a good idea to pack all the extraction logic within its own page
object. Let's do so with the former example. We are going to create
a new page object ``UPCProductPage`` that will depend on both
``AutoExtractWebPage`` (by inheritance) and ``AutoExtractProductPage``
(by membership).

.. code-block:: python

    class UPCProductPage(AutoExtractWebPage):

        product_page: AutoExtractProductPage

        def to_item():
            product = self.product_page.to_item()
            my_product = UPCProduct.from_dict(attr.asdict(product))
            my_product.upc = self.css("tr:nth-child(1) td::text").get()
            return my_product

Note that the methods ``css`` and ``xpath`` are available through ``self``.

See the `scrapy-poet tutorial<https://scrapy-poet.readthedocs.io/en/stable/intro/tutorial.html>`_
to learn more about page objects and understand better the example above.

And how does the spider look like now?. Here you can see it:

.. code-block:: python

    class ProductSpider(scrapy.Spider):

        name = "products"
        start_urls = ['https://books.toscrape.com/catalogue/sharp-objects_997/index.html']

        def parse(self, response: DummyReponse, product_page: UPCProductPage):
            yield product_page.to_item()

The spider is now very simple because all the extraction logic has been moved
to the new page object ``UPCProductPage``.

Compatibility with new fields added to the API
----------------------------------------------

Eventually, some new fields could be added to the API.
Your code using ``autoextract-poet`` would ignore them by default
until you upgrade the library to a version containing the new field.
But you might want to write code that automatically include those
unknown attributes in the spider output even if you don't update
the ``autoextract-poet`` library. This is possible
because ``autoextract-poet`` items preserve those unknown
fields in the private property ``_unknown_fields_dict``.

If you want these unknown attributes to be exposed in the output,
you only have to use the following pipeline in your Scrapy project:

.. code-block:: python

    from autoextract_poet import AutoExtractAdapter
    from itemadapter import ItemAdapter


    class AutoExtractPipeline:
        def open_spider(self, spider):
            # Serialization for autoextract-poet items
            ItemAdapter.ADAPTER_CLASSES.appendleft(AutoExtractAdapter)

        def process_item(self, item, spider):
            return ItemAdapter(item).asdict()

        def close_spider(self, spider):
            ItemAdapter.ADAPTER_CLASSES.remove(AutoExtractAdapter)

The :py:class:`autoextract-poet.adapters.AutoExtractAdapter` is responsible
for ensuring that all the attributes in ``_unknown_fields_dict`` are also present
in the resultant item.

Note that, in this setup, you could use ``_unknown_fields_dict`` to add new attributes
to an item very easily. For example, the ``UPCProductPage`` could have
been rewritten as:


.. code-block:: python

    class UPCProductPage(AutoExtractWebPage):

        product_page: AutoExtractProductPage

        def to_item():
            product = self.product_page.to_item()
            upc = self.css("tr:nth-child(1) td::text").get()
            product._unknown_fields_dict["upc"] = upc
            return my_product

This has the advantage that you don't have to create the
item class `UPCProduct`, so it requires much less code.

In any case, we don't recommend doing it. Extending the original
item to add new attributes might be more verbose, but has the additional
benefits that it provides validation for the fields at
three different levels: IDE, typing checkers (e.g. ``mypy``) and
runtime (by the use of the ``slots=True`` facility). What is more, you'll
get code completion for the new attributes in your favourite IDE.
It will then encourage healthier code.


.. _web-poet: https://github.com/scrapinghub/web-poet
.. _andi: https://github.com/scrapinghub/andi
.. _parsel: https://github.com/scrapinghub/parsel
.. _scrapy-autoextract: https://github.com/scrapinghub/scrapy-autoextract
.. _`AutoExtract API`: https://docs.zyte.com/automatic-extraction.html
.. _`scrapy-poet`: https://scrapy-poet.readthedocs.io/en/stable/
