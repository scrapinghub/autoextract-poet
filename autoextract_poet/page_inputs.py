from typing import ClassVar, Generic, Optional, TypeVar

import attr

from autoextract_poet.items import (
    Article,
    Item,
    Product, ProductList, ArticleList, Comments, ForumPosts, JobPosting,
    RealEstate, Reviews, Vehicle,
)
from autoextract_poet.util import export


@export
@attr.s(auto_attribs=True)
class AutoExtractHtml:
    """A container for URL and HTML content retrieved from AutoExtract.

    ``url`` should be an URL of the response (after all redirects),
    not an URL of the request, if possible.

    ``html`` should be browser HTML in unicode
    """
    url: str
    html: str


T = TypeVar("T", bound=Item)


@attr.s(auto_attribs=True)
class AutoExtractData(Generic[T]):
    """Container for AutoExtract data.

    Should not be used directly by providers.
    Use derived classes like AutoExtractArticleData and similar.

    API responses are wrapped in a JSON array
    (this is to facilitate query batching)
    but we're receiving single responses here..

    https://docs.zyte.com/automatic-extraction.html#responses
    """
    page_type: ClassVar[str]
    data: dict

    @property
    def item_class(self):
        return self.__orig_bases__[0].__args__[0]

    def to_item(self) -> Optional[T]:
        return self.item_class.from_dict(self.data[self.page_type])


@export
@attr.s(auto_attribs=True)
class AutoExtractArticleData(AutoExtractData[Article]):
    """Container for AutoExtract Article data.

    https://docs.zyte.com/automatic-extraction/article.html
    """
    page_type = "article"


@export
@attr.s(auto_attribs=True)
class AutoExtractProductData(AutoExtractData[Product]):
    """Container for AutoExtract Product data.

    https://docs.zyte.com/automatic-extraction/product.html
    """
    page_type = "product"


@export
@attr.s(auto_attribs=True)
class AutoExtractProductListData(AutoExtractData[ProductList]):
    """Container for AutoExtract Product list data.

    https://docs.zyte.com/automatic-extraction/product-list.html
    """
    page_type = "productList"


@export
@attr.s(auto_attribs=True)
class AutoExtractArticleListData(AutoExtractData[ArticleList]):
    """Container for AutoExtract Article list data.

    https://docs.zyte.com/automatic-extraction/article-list.html
    """
    page_type = "articleList"


@export
@attr.s(auto_attribs=True)
class AutoExtractCommentsData(AutoExtractData[Comments]):
    """Container for AutoExtract Comments data.

    https://docs.zyte.com/automatic-extraction/comment.html
    """
    page_type = "comments"


@export
@attr.s(auto_attribs=True)
class AutoExtractForumPostsData(AutoExtractData[ForumPosts]):
    """Container for AutoExtract Forum Posts data.

    https://docs.zyte.com/automatic-extraction/forum-post.html
    """
    page_type = "forumPosts"


@export
@attr.s(auto_attribs=True)
class AutoExtractJobPostingData(AutoExtractData[JobPosting]):
    """Container for AutoExtract Job Posting data.

    https://docs.zyte.com/automatic-extraction/job-posting.html
    """
    page_type = "jobPosting"


@export
@attr.s(auto_attribs=True)
class AutoExtractRealEstateData(AutoExtractData[RealEstate]):
    """Container for AutoExtract Real Estate data.

    https://docs.zyte.com/automatic-extraction/real-estate.html
    """
    page_type = "realEstate"


@export
@attr.s(auto_attribs=True)
class AutoExtractReviewsData(AutoExtractData[Reviews]):
    """Container for AutoExtract Reviews data.

    https://docs.zyte.com/automatic-extraction/review.html
    """
    page_type = "reviews"


@export
@attr.s(auto_attribs=True)
class AutoExtractVehicleData(AutoExtractData[Vehicle]):
    """Container for AutoExtract Vehicle data.

    https://docs.zyte.com/automatic-extraction/vehicle.html
    """
    page_type = "vehicle"
