import attr
import pytest

from autoextract_poet.items import (
    AdditionalProperty,
    Article,
    Breadcrumb,
    GTIN,
    Offer,
    Product,
    Rating, ProductList, PaginationLink, Item,
)

from tests import load_fixture, temp_seed, crazy_monkey_nullify

example_article_result = load_fixture("sample_article.json")[0]
example_product_result = load_fixture("sample_product.json")[0]
example_product_list_result = load_fixture("sample_product_list.json")[0]


@pytest.mark.parametrize(
    "cls, data",
    [(Offer, offer) for offer in example_product_result["product"]["offers"]] +  # type: ignore
    [(Breadcrumb, breadcrumb) for breadcrumb in example_product_result["product"]["breadcrumbs"]] +  # type: ignore
    [(AdditionalProperty, additionalProperty) for additionalProperty in example_product_result["product"]["additionalProperty"]] +  # type: ignore
    [(GTIN, gtin) for gtin in example_product_result["product"]["gtin"]] +  # type: ignore
    [(Rating, example_product_result["product"]["aggregateRating"])] +  # type: ignore
    [(Product, example_product_result["product"])] +  # type: ignore
    [(Article, example_article_result["article"])] + # type: ignore
    [(PaginationLink, example_product_list_result["productList"]["paginationNext"])] +  # type: ignore
    [(ProductList, example_product_list_result["productList"])]  # type: ignore
)  # type: ignore
@pytest.mark.parametrize(
    "unexpected_attrs",
    [{}, {"unexpected_attribute": "Should not fail"}]
)  # type: ignore
def test_item(cls, data, unexpected_attrs):
    item = cls.from_dict({**data, **unexpected_attrs})
    assert attr.asdict(item) == data
    assert item._additional_attrs == unexpected_attrs

    with temp_seed(7):
        for _ in range(10):
            data_with_holes = crazy_monkey_nullify(data)
            item = cls.from_dict(data_with_holes)
            assert attr.asdict(item) == data_with_holes

    # AttributeError: 'cls' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        cls(**data, foo="bar")


def test_from_list():

    @attr.s(auto_attribs=True, slots=True)
    class Number(Item):
        value: int

    actual = Number.from_list([None, dict(value=1), None, dict(value=2)])
    expected = [None, Number(1), None, Number(2)]
    assert actual == expected

    assert Number.from_list(None) == []
    assert Number.from_list([]) == []