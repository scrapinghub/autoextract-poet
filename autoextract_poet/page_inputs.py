from typing import ClassVar, Generic, Optional, Type, TypeVar

import attr

from autoextract_poet.items import (
    Article,
    Item,
    Product,
)

T = TypeVar("T", bound=Item)


@attr.s(auto_attribs=True)
class _AutoExtractData(Generic[T]):
    """Container for AutoExtract data.

    Should not be used directly by providers.
    Use derived classes like AutoExtractArticleData and similar.

    API responses are wrapped in a JSON array
    (this is to facilitate query batching)
    but we're receiving single responses here..

    https://doc.scrapinghub.com/autoextract.html#responses
    """

    _item_key: ClassVar[str]

    data: dict

    @property
    def item_class(self):
        return self.__orig_bases__[0].__args__[0]

    def to_item(self) -> Optional[T]:
        return self.item_class.from_dict(self.data[self._item_key])


@attr.s(auto_attribs=True)
class AutoExtractArticleData(_AutoExtractData[Article]):
    """Container for AutoExtract Article data.

    https://doc.scrapinghub.com/autoextract/article.html
    """

    _item_key = "article"


@attr.s(auto_attribs=True)
class AutoExtractProductData(_AutoExtractData[Product]):
    """Container for AutoExtract Product data.

    https://doc.scrapinghub.com/autoextract/product.html
    """

    _item_key = "product"