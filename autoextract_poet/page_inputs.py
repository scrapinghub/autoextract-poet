from typing import ClassVar, List, Optional, Type

import attr

from autoextract_poet.items import (
    Article,
    Item,
    Product,
)


@attr.s(auto_attribs=True)
class ResponseData:
    """Container for AutoExtract response data.

    Should not be used directly by providers.
    Use derived classes like ArticleResponseData and similar.

    API responses are wrapped in a JSON array
    (this is to facilitate query batching).

    https://doc.scrapinghub.com/autoextract.html#responses
    """

    item_class: ClassVar[Type[Item]]
    item_key: ClassVar[str]

    data: dict

    def to_items(self) -> Optional[List[Item]]:
        return self.item_class.from_list(
            [
                query_result[self.item_key]
                for query_result in self.data
                if "error" not in query_result
            ]
        )


@attr.s(auto_attribs=True)
class ArticleResponseData(ResponseData):
    """Container for AutoExtract Article response data.

    https://doc.scrapinghub.com/autoextract/article.html
    """

    item_class = Article
    item_key = "article"


@attr.s(auto_attribs=True)
class ProductResponseData(ResponseData):
    """Container for AutoExtract Product response data.

    https://doc.scrapinghub.com/autoextract/product.html
    """

    item_class = Product
    item_key = "product"
