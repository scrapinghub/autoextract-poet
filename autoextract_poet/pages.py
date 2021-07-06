from typing import Optional

import attr

from autoextract_poet.items import Article, Product, ProductList, ArticleList, \
    Comments, ForumPosts, JobPosting, RealEstate, Reviews, Vehicle
from autoextract_poet.page_inputs import AutoExtractHtml, \
    AutoExtractProductData, AutoExtractProductListData, AutoExtractArticleData, \
    T, AutoExtractArticleListData, AutoExtractCommentsData, \
    AutoExtractForumPostsData, AutoExtractJobPostingData, \
    AutoExtractRealEstateData, AutoExtractReviewsData, AutoExtractVehicleData
from autoextract_poet.util import export
from web_poet import Injectable, ItemPage
from web_poet.mixins import ResponseShortcutsMixin


@export
@attr.s(auto_attribs=True)
class AutoExtractWebPage(Injectable, ResponseShortcutsMixin):
    """Base Page Object which requires :class:`~.AutoExtractHtml`
    and provides XPath / CSS shortcuts.

    Use this class as a base class for Page Objects which work on
    the browser HTML provided by AutoExtract.
    """
    response: AutoExtractHtml


@export
@attr.s(auto_attribs=True)
class AutoExtractItemWebPage(AutoExtractWebPage, ItemPage):
    """:class:`AutoExtractWebPage` that requires the :meth:`to_item` method to
    be implemented.
    """
    pass


@export
@attr.s(auto_attribs=True)
class AutoExtractArticlePage(ItemPage):
    """
    Article data from AutoExtract

    https://docs.zyte.com/automatic-extraction/article.html
    """
    article_data: AutoExtractArticleData

    def to_item(self) -> Optional[Article]:
        return self.article_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractArticleListPage(ItemPage):
    """
    Article list data from AutoExtract

    https://docs.zyte.com/automatic-extraction/article-list.html
    """
    article_list_data: AutoExtractArticleListData

    def to_item(self) -> Optional[ArticleList]:
        return self.article_list_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractProductPage(ItemPage):
    """
    Product data from AutoExtract

    https://docs.zyte.com/automatic-extraction/product.html
    """
    product_data: AutoExtractProductData

    def to_item(self) -> Optional[Product]:
        return self.product_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractProductListPage(ItemPage):
    """
    Product list data from AutoExtract

    https://docs.zyte.com/automatic-extraction/product-list.html
    """
    product_list_data: AutoExtractProductListData

    def to_item(self) -> Optional[ProductList]:
        return self.product_list_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractCommentsPage(ItemPage):
    """
    Comments data from AutoExtract

    https://docs.zyte.com/automatic-extraction/comment.html
    """
    comments_data: AutoExtractCommentsData

    def to_item(self) -> Optional[Comments]:
        return self.comments_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractForumPostsPage(ItemPage):
    """
    Forum posts data from AutoExtract

    https://docs.zyte.com/automatic-extraction/forum-post.html
    """
    forum_posts_data: AutoExtractForumPostsData

    def to_item(self) -> Optional[ForumPosts]:
        return self.forum_posts_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractJobPostingPage(ItemPage):
    """
    Job posting data from AutoExtract

    https://docs.zyte.com/automatic-extraction/job-posting.html
    """
    job_posting_data: AutoExtractJobPostingData

    def to_item(self) -> Optional[JobPosting]:
        return self.job_posting_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractRealEstatePage(ItemPage):
    """
    Real estate data from AutoExtract

    https://docs.zyte.com/automatic-extraction/real-estate.html
    """
    real_estate_data: AutoExtractRealEstateData

    def to_item(self) -> Optional[RealEstate]:
        return self.real_estate_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractReviewsPage(ItemPage):
    """
    Reviews data from AutoExtract

    https://docs.zyte.com/automatic-extraction/review.html
    """
    reviews_data: AutoExtractReviewsData

    def to_item(self) -> Optional[Reviews]:
        return self.reviews_data.to_item()


@export
@attr.s(auto_attribs=True)
class AutoExtractVehiclePage(ItemPage):
    """
    Vehicle data from AutoExtract

    https://docs.zyte.com/automatic-extraction/vehicle.html
    """
    vehicle_data: AutoExtractVehicleData

    def to_item(self) -> Optional[Vehicle]:
        return self.vehicle_data.to_item()
