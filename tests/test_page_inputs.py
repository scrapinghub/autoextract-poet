import attr
import pytest

from autoextract_poet import *

from tests import load_fixture

example_article_result = load_fixture("sample_article.json")
example_product_result = load_fixture("sample_product.json")
example_product_list_result = load_fixture("sample_product_list.json")


@pytest.mark.parametrize("page_input_cls, page_cls, results", [
    (AutoExtractArticleData, AutoExtractArticlePage, example_article_result),
    (AutoExtractProductData, AutoExtractProductPage, example_product_result),
    (AutoExtractProductListData, AutoExtractProductListPage, example_product_list_result),
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