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
