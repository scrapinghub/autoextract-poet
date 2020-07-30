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

# https://doc.scrapinghub.com/autoextract/article.html
example_article_result = {
    "article": {
        "headline": "Article headline",
        "datePublished": "2019-06-19T00:00:00",
        "datePublishedRaw": "June 19, 2019",
        "dateModified": "2019-06-21T00:00:00",
        "dateModifiedRaw": "June 21, 2019",
        "author": "Article author",
        "authorsList": [
            "Article author"
        ],
        "inLanguage": "en",
        "breadcrumbs": [
            {
                "name": "Level 1",
                "link": "http://example.com"
            }
        ],
        "mainImage": "http://example.com/image.png",
        "images": [
            "http://example.com/image.png"
        ],
        "description": "Article summary",
        "articleBody": "Article body ...",
        "articleBodyHtml": "<article><p>Article body ... </p> ... </article>",
        "articleBodyRaw": "<div id=\"an-article\">Article body ...",
        "videoUrls": [
            "https://example.com/video.mp4"
        ],
        "audioUrls": [
            "https://example.com/audio.mp3"
        ],
        "probability": 0.95,
        "canonicalUrl": "https://example.com/article/article-about-something",
        "url": "https://example.com/article?id=24"
    },
    "webPage": {
        "inLanguages": [
            {"code": "en"},
            {"code": "es"}
        ]
    },
    "query": {
        "id": "1564747029122-9e02a1868d70b7a3",
        "domain": "example.com",
        "userQuery": {
            "pageType": "article",
            "url": "http://example.com/article?id=24"
        }
    }
}

# https://doc.scrapinghub.com/autoextract/product.html
example_product_result = {
    "product": {
        "name": "Product name",
        "offers": [
            {
                "price": "42",
                "currency": "USD",
                "availability": "InStock"
            }
        ],
        "sku": "product sku",
        "mpn": "product mpn",
        "gtin": [
            {
                "type": "ean13",
                "value": "978-3-16-148410-0"
            }
        ],
        "brand": "product brand",
        "breadcrumbs": [
            {
                "name": "Level 1",
                "link": "http://example.com"
            }
        ],
        "mainImage": "http://example.com/image.png",
        "images": [
            "http://example.com/image.png"
        ],
        "description": "product description",
        "aggregateRating": {
            "ratingValue": 4.5,
            "bestRating": 5.0,
            "reviewCount": 31
        },
        "additionalProperty": [
            {
                "name": "property 1",
                "value": "value of property 1"
            }
        ],
        "probability": 0.95,
        "url": "https://example.com/product"
    },
    "webPage": {
        "inLanguages": [
            {"code": "en"},
            {"code": "es"}
        ]
    },
    "query": {
        "id": "1564747029122-9e02a1868d70b7a2",
        "domain": "example.com",
        "userQuery": {
            "pageType": "product",
            "url": "https://example.com/product"
        }
    }
}


@pytest.mark.parametrize("offer", example_product_result["product"]["offers"])  # type: ignore
def test_offer(offer):
    item = Offer.from_dict(offer)
    for key, value in offer.items():
        assert getattr(item, key) == value

    # AttributeError: 'Offer' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        Offer(**offer, foo="bar")


@pytest.mark.parametrize("breadcrumb", example_product_result["product"]["breadcrumbs"])  # type: ignore
def test_breadcrumb(breadcrumb):
    item = Breadcrumb.from_dict(breadcrumb)
    for key, value in breadcrumb.items():
        assert getattr(item, key) == value

    # AttributeError: 'Breadcrumb' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        Breadcrumb(**breadcrumb, foo="bar")


@pytest.mark.parametrize("additional_property", example_product_result["product"]["additionalProperty"])  # type: ignore
def test_additional_property(additional_property):
    item = AdditionalProperty.from_dict(additional_property)
    for key, value in additional_property.items():
        assert getattr(item, key) == value

    # AttributeError: 'AdditionalProperty' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        AdditionalProperty(**additional_property, foo="bar")


@pytest.mark.parametrize("gtin", example_product_result["product"]["gtin"])  # type: ignore
def test_gtin(gtin):
    item = GTIN.from_dict(gtin)
    for key, value in gtin.items():
        assert getattr(item, key) == value

    # AttributeError: 'GTIN' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        GTIN(**gtin, foo="bar")


def test_rating():
    rating = example_product_result["product"]["aggregateRating"]
    item = Rating.from_dict(rating)
    for key, value in rating.items():
        assert getattr(item, key) == value

    # AttributeError: 'Rating' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        Rating(**rating, foo="bar")


def test_product():
    product = example_product_result["product"]
    item = Product.from_dict(product)
    for key, value in product.items():
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

    # AttributeError: 'Product' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        Product(**product, foo="bar")


def test_article():
    article = example_article_result["article"]
    item = Article.from_dict(article)
    for key, value in article.items():
        if key == 'breadcrumbs':
            value = Breadcrumb.from_list(value)

        assert getattr(item, key) == value

    # AttributeError: 'Article' object has no attribute 'foo'
    with pytest.raises(AttributeError):
        item.foo = "bar"

    # TypeError: __init__() got an unexpected argument 'foo'
    with pytest.raises(TypeError):
        Article(**article, foo="bar")
