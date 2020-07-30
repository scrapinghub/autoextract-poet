from typing import Dict, List, Optional, Tuple

import attr


class Item:

    def __setattr__(self, key, value):
        if key not in self.__slots__:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has not attribute '{key}'"
            )

        super().__setattr__(key, value)

    @classmethod
    def from_dict(cls, item_dict: dict):
        return cls(**item_dict) if item_dict else None


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
