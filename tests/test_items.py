import pytest

from autoextract_poet.items import (
    Offer,
    Breadcrumb,
    Rating,
    AdditionalProperty,
    GTIN,
    Article,
    Product,
)

from tests import load_fixture

example_product_result = load_fixture("sample_product.json")
example_article_result = load_fixture("sample_article.json")


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
    for key, value in data.items():
        if key == 'breadcrumbs':
            value = Breadcrumb.from_list(value)
        if key == 'offers':
            value = Offer.from_list(value)
        if key == 'additionalProperty':
            value = AdditionalProperty.from_list(value)
        if key == 'gtin':
            value = GTIN.from_list(value)
        if key == 'aggregateRating':
            value = Rating.from_dict(value)

        assert getattr(item, key) == value

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
