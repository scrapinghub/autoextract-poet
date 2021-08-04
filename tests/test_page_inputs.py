import attr
import pytest

from autoextract_poet import *
from autoextract_poet.page_inputs import AutoExtractArticleListData, \
    AutoExtractJobPostingData, AutoExtractCommentsData, \
    AutoExtractForumPostsData, AutoExtractRealEstateData, \
    AutoExtractReviewsData, AutoExtractVehicleData
from autoextract_poet.pages import AutoExtractArticleListPage, \
    AutoExtractJobPostingPage, AutoExtractCommentsPage, \
    AutoExtractForumPostsPage, AutoExtractRealEstatePage, \
    AutoExtractReviewsPage, AutoExtractVehiclePage

from tests import load_fixture

example_article_result = load_fixture("sample_article.json")
example_article_list_result = load_fixture("sample_article_list.json")
example_product_result = load_fixture("sample_product.json")
example_product_list_result = load_fixture("sample_product_list.json")
example_job_posting_result = load_fixture("sample_job_posting.json")
example_comments_result = load_fixture("sample_comments.json")
example_forum_posts_result = load_fixture("sample_forum_posts.json")
example_real_estate_result = load_fixture("sample_real_estate.json")
example_reviews_result = load_fixture("sample_reviews.json")
example_vehicle_result = load_fixture("sample_vehicle.json")


@pytest.mark.parametrize("page_input_cls, page_cls, results", [
    (AutoExtractArticleData, AutoExtractArticlePage, example_article_result),
    (AutoExtractArticleListData, AutoExtractArticleListPage, example_article_list_result),
    (AutoExtractProductData, AutoExtractProductPage, example_product_result),
    (AutoExtractProductListData, AutoExtractProductListPage, example_product_list_result),
    (AutoExtractJobPostingData, AutoExtractJobPostingPage, example_job_posting_result),
    (AutoExtractCommentsData, AutoExtractCommentsPage, example_comments_result),
    (AutoExtractForumPostsData, AutoExtractForumPostsPage, example_forum_posts_result),
    (AutoExtractRealEstateData, AutoExtractRealEstatePage, example_real_estate_result),
    (AutoExtractReviewsData, AutoExtractReviewsPage, example_reviews_result),
    (AutoExtractVehicleData, AutoExtractVehiclePage, example_vehicle_result),
])
def test_response_data_and_page(page_input_cls, page_cls, results):
    response_data = page_input_cls(results[0])
    item = response_data.to_item()
    assert isinstance(item, response_data.item_class)
    expected = results[0][page_input_cls.page_type]
    assert attr.asdict(item) == expected
    assert attr.asdict(page_cls(response_data).to_item()) == expected


def test_auto_extract_html():
    url = "https://example.com"
    html = "<html><body><p>Hello!</p></body></html>"
    data = AutoExtractHtml(url, html)
    assert data.url == url
    assert data.html == html
    assert AutoExtractHtml(url, html) == data