import pytest

from autoextract_poet.page_inputs import (
    AutoExtractArticleData,
    AutoExtractProductData,
)

from tests import load_fixture, compare_item_with_dict

example_article_result = load_fixture("sample_article.json")
example_product_result = load_fixture("sample_product.json")


@pytest.mark.parametrize("cls, results", [
    (AutoExtractArticleData, example_article_result),
    (AutoExtractProductData, example_product_result),
])
def test_response_data(cls, results):
    response_data = cls(results)
    items = response_data.to_items()
    assert len(items) == 1
    assert type(items[0]) == cls.item_class
    assert compare_item_with_dict(items[0], results[0][cls.item_key])
