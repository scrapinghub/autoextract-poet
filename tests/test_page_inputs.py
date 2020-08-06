import pytest

from autoextract_poet.page_inputs import (
    AutoExtractArticleData,
    AutoExtractProductData,
)

from tests import load_fixture, compare_item_with_dict

example_article_result = load_fixture("sample_article.json")
example_product_result = load_fixture("sample_product.json")


@pytest.mark.parametrize("cls, results, page_type", [
    (AutoExtractArticleData, example_article_result, "article"),
    (AutoExtractProductData, example_product_result, "product"),
])
def test_response_data(cls, results, page_type):
    response_data = cls(results[0][page_type])
    item = response_data.to_item()
    assert isinstance(item, cls.item_class)
    assert compare_item_with_dict(item, results[0][cls.item_key])
