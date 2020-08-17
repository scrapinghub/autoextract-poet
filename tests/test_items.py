import pytest

from autoextract_poet.items import (
    AdditionalProperty,
    Article,
    Breadcrumb,
    GTIN,
    Offer,
    Product,
    Rating,
)

from tests import load_fixture, item_equals_dict

example_article_result = load_fixture("sample_article.json")[0]
example_product_result = load_fixture("sample_product.json")[0]


@pytest.mark.parametrize(
    "cls, data",
    [(Offer, offer) for offer in example_product_result["product"]["offers"]] +  # type: ignore
    [(Breadcrumb, breadcrumb) for breadcrumb in example_product_result["product"]["breadcrumbs"]] +  # type: ignore
    [(AdditionalProperty, additionalProperty) for additionalProperty in example_product_result["product"]["additionalProperty"]] +  # type: ignore
    [(GTIN, gtin) for gtin in example_product_result["product"]["gtin"]] +  # type: ignore
    [(Rating, example_product_result["product"]["aggregateRating"])] +  # type: ignore
    [(Product, example_product_result["product"])] +  # type: ignore
    [(Article, example_article_result["article"])]  # type: ignore
)  # type: ignore
def test_item(cls, data):
    item = cls.from_dict(data)
    assert item_equals_dict(item, data)

    # AttributeError: 'cls' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        cls(**data, foo="bar")

    new_data = dict(**data)
    new_data["foo"] = "bar"
    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        cls.from_dict(new_data)
