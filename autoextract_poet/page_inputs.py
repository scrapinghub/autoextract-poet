from typing import ClassVar, Optional, Type

import attr

from autoextract_poet.items import (
    Article,
    Item,
    Product,
)


@attr.s(auto_attribs=True)
class _AutoExtractData:
    """Container for AutoExtract data.

    Should not be used directly by providers.
    Use derived classes like AutoExtractArticleData and similar.

    API responses are wrapped in a JSON array
    (this is to facilitate query batching)
    but we're receiving single responses here..

    https://doc.scrapinghub.com/autoextract.html#responses
    """

    item_class: ClassVar[Type[Item]]
    item_key: ClassVar[str]

    data: dict

    def to_item(self) -> Optional[Item]:
        return self.item_class.from_dict(self.data)


@attr.s(auto_attribs=True)
class AutoExtractArticleData(_AutoExtractData):
    """Container for AutoExtract Article data.

    https://doc.scrapinghub.com/autoextract/article.html
    """

    item_class = Article
    item_key = "article"


@attr.s(auto_attribs=True)
class AutoExtractProductData(_AutoExtractData):
    """Container for AutoExtract Product data.

    https://doc.scrapinghub.com/autoextract/product.html
    """

    item_class = Product
    item_key = "product"
