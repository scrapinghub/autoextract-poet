import attr
import pytest

from autoextract_poet import (
    AutoExtractArticleData,
    AutoExtractProductData,
    AutoExtractHtml,
)

from tests import load_fixture

example_article_result = load_fixture("sample_article.json")
example_product_result = load_fixture("sample_product.json")


@pytest.mark.parametrize("cls, results", [
    (AutoExtractArticleData, example_article_result),
    (AutoExtractProductData, example_product_result),
])
def test_response_data(cls, results):
    response_data = cls(results[0])
    item = response_data.to_item()
    assert isinstance(item, response_data.item_class)
    assert attr.asdict(item) == results[0][cls.page_type]


def test_auto_extract_html():
    url = "https://example.com"
    html = "<html><body><p>Hello!</p></body></html>"
    data = AutoExtractHtml(url, html)
    assert data.url == url
    assert data.html == html
    assert AutoExtractHtml(url, html) == data