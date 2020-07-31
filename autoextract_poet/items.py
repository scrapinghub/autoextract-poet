from typing import Dict, List, Optional

import attr


@attr.s(auto_attribs=True, slots=True)
class Item:

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        return cls(**item) if item else None  # type: ignore

    @classmethod
    def from_list(cls, items: List[Dict]):
        return [cls.from_dict(item) for item in items if item]


@attr.s(auto_attribs=True, slots=True)
class Offer(Item):

    price: Optional[str] = None
    currency: Optional[str] = None
    availability: Optional[str] = None
    regularPrice: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Breadcrumb(Item):

    name: Optional[str] = None
    link: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Rating(Item):

    ratingValue: Optional[float]
    bestRating: Optional[float]
    reviewCount: Optional[int]


@attr.s(auto_attribs=True, slots=True)
class AdditionalProperty(Item):

    name: str
    value: str


@attr.s(auto_attribs=True, slots=True)
class GTIN(Item):

    type: str
    value: str


@attr.s(auto_attribs=True, slots=True)
class Article(Item):

    headline: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    dateModified: Optional[str] = None
    dateModifiedRaw: Optional[str] = None
    author: Optional[str] = None
    authorsList: Optional[List[str]] = None
    inLanguage: Optional[str] = None
    breadcrumbs: Optional[List[Breadcrumb]] = None
    mainImage: Optional[str] = None
    images: Optional[List[str]] = None
    description: Optional[str] = None
    articleBody: Optional[str] = None
    articleBodyHtml: Optional[str] = None
    articleBodyRaw: Optional[str] = None
    videoUrls: Optional[List[str]] = None
    audioUrls: Optional[List[str]] = None
    probability: Optional[float] = None
    canonicalUrl: Optional[str] = None
    url: Optional[str] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        if not item:
            return None

        new_item = dict(**item)
        new_item.update(dict(
            breadcrumbs=Breadcrumb.from_list(item.get("breadcrumbs", [])),
        ))

        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class Product(Item):

    name: Optional[str] = None
    offers: Optional[List[Offer]] = None
    sku: Optional[str] = None
    gtin: Optional[List[GTIN]] = None
    mpn: Optional[str] = None
    brand: Optional[str] = None
    breadcrumbs: Optional[List[Breadcrumb]] = None
    mainImage: Optional[str] = None
    images: Optional[List[str]] = None
    description: Optional[str] = None
    probability: Optional[float] = None
    url: Optional[str] = None
    additionalProperty: Optional[List[AdditionalProperty]] = None
    aggregateRating: Optional[Rating] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        if not item:
            return None

        new_item = dict(**item)
        new_item.update(dict(
            additionalProperty=AdditionalProperty.from_list(
                item.get("additionalProperty", [])),
            aggregateRating=Rating.from_dict(item.get("aggregateRating")),
            breadcrumbs=Breadcrumb.from_list(item.get("breadcrumbs", [])),
            gtin=GTIN.from_list(item.get("gtin", [])),
            offers=Offer.from_list(item.get("offers", [])),
        ))

        return super().from_dict(new_item)
