from typing import Optional

import attr

from autoextract_poet.items import Article, Product, ProductList
from autoextract_poet.page_inputs import AutoExtractHtml, \
    AutoExtractProductData, AutoExtractProductListData, AutoExtractArticleData, \
    T
from web_poet import Injectable, ItemPage
from web_poet.mixins import ResponseShortcutsMixin


@attr.s(auto_attribs=True)
class AutoExtractWebPage(Injectable, ResponseShortcutsMixin):
    """Base Page Object which requires :class:`~.AutoExtractHtml`
    and provides XPath / CSS shortcuts.

    Use this class as a base class for Page Objects which work on
    the browser HTML provided by AutoExtract.
    """
    response: AutoExtractHtml


@attr.s(auto_attribs=True)
class AutoExtractItemWebPage(AutoExtractWebPage, ItemPage):
    """:class:`AutoExtractWebPage` that requires the :meth:`to_item` method to
    be implemented.
    """
    pass


@attr.s(auto_attribs=True)
class AutoExtractArticlePage(ItemPage):
    """
    Article data from AutoExtract

    https://docs.zyte.com/automatic-extraction/article.html
    """
    article_data: AutoExtractArticleData

    def to_item(self) -> Optional[Article]:
        return self.article_data.to_item()


@attr.s(auto_attribs=True)
class AutoExtractProductPage(ItemPage):
    """
    Product data from AutoExtract

    https://docs.zyte.com/automatic-extraction/product.html
    """
    product_data: AutoExtractProductData

    def to_item(self) -> Optional[Product]:
        return self.product_data.to_item()


@attr.s(auto_attribs=True)
class AutoExtractProductListPage(ItemPage):
    """
    Product list data from AutoExtract

    https://docs.zyte.com/automatic-extraction/product-list.html
    """
    product_list_data: AutoExtractProductListData

    def to_item(self) -> Optional[ProductList]:
        return self.product_list_data.to_item()

