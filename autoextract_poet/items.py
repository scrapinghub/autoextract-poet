from typing import Dict, List, Optional, Tuple

import attr


@attr.s(auto_attribs=True, slots=True)
class Offer:

    price: Optional[str] = None
    currency: Optional[str] = None
    availability: Optional[str] = None
    regularPrice: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Breadcrumb:

    name: Optional[str] = None
    link: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Rating:

    ratingValue: Optional[float]
    bestRating: Optional[float]
    reviewCount: Optional[int]


@attr.s(auto_attribs=True, slots=True)
class AdditionalProperty:

    name: str
    value: str


@attr.s(auto_attribs=True, slots=True)
class GTIN:

    type: str
    value: str


@attr.s(auto_attribs=True, slots=True)
class Article:

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
class Product:

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
