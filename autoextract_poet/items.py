from typing import Dict, List, Optional

import attr

from autoextract_poet.util import remove_unknown_fields


@attr.s(auto_attribs=True, slots=True)
class Item:

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        """
        Read an item from a dictionary, ignoring unknown attributes for
        backwards compatibility
        """
        item = remove_unknown_fields(item, cls)
        return cls(**item) if item else None  # type: ignore

    @classmethod
    def from_list(cls, items: Optional[List[Dict]]) -> List:
        """
        Read items from a list, ignoring unknown attributes for
        backwards compatibility
        """
        return [cls.from_dict(item) for item in items or []]


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

    ratingValue: Optional[float] = None
    bestRating: Optional[float] = None
    reviewCount: Optional[int] = None


@attr.s(auto_attribs=True, slots=True)
class AdditionalProperty(Item):

    name: str
    value: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class GTIN(Item):

    type: str
    value: str


@attr.s(auto_attribs=True, slots=True)
class Article(Item):

    url: Optional[str] = None
    probability: Optional[float] = None
    headline: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    dateModified: Optional[str] = None
    dateModifiedRaw: Optional[str] = None
    author: Optional[str] = None
    authorsList: List[str] = attr.Factory(list)
    inLanguage: Optional[str] = None
    breadcrumbs: List[Breadcrumb] = attr.Factory(list)
    mainImage: Optional[str] = None
    images: List[str] = attr.Factory(list)
    description: Optional[str] = None
    articleBody: Optional[str] = None
    articleBodyHtml: Optional[str] = None
    articleBodyRaw: Optional[str] = None
    videoUrls: List[str] = attr.Factory(list)
    audioUrls: List[str] = attr.Factory(list)
    canonicalUrl: Optional[str] = None


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

    url: Optional[str] = None
    probability: Optional[float] = None
    name: Optional[str] = None
    offers: List[Offer] = attr.Factory(list)
    sku: Optional[str] = None
    gtin: List[GTIN] = attr.Factory(list)
    mpn: Optional[str] = None
    brand: Optional[str] = None
    breadcrumbs: List[Breadcrumb] = attr.Factory(list)
    mainImage: Optional[str] = None
    images: List[str] = attr.Factory(list)
    description: Optional[str] = None
    additionalProperty: List[AdditionalProperty] = attr.Factory(list)
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


@attr.s(auto_attribs=True, slots=True)
class ProductFromList(Item):

    probability: Optional[float] = None
    url: Optional[str] = None
    name: Optional[str] = None
    offers: List[Offer] = attr.Factory(list)
    sku: Optional[str] = None
    brand: Optional[str] = None
    mainImage: Optional[str] = None
    images: List[str] = attr.Factory(list)
    description: Optional[str] = None
    aggregateRating: Optional[Rating] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        if not item:
            return None

        new_item = dict(**item)
        new_item.update(dict(
            aggregateRating=Rating.from_dict(item.get("aggregateRating")),
            offers=Offer.from_list(item.get("offers", [])),
        ))

        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class PaginationLink(Item):

    url: Optional[str] = None
    text: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class ProductList(Item):

    url: Optional[str] = None
    products: List[ProductFromList] = attr.Factory(list)
    breadcrumbs: List[Breadcrumb] = attr.Factory(list)
    paginationNext: Optional[PaginationLink] = None
    paginationPrevious: Optional[PaginationLink] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        if not item:
            return None

        new_item = dict(**item)
        new_item.update(dict(
            products=ProductFromList.from_list(item.get("products", [])),
            breadcrumbs=Breadcrumb.from_list(item.get("breadcrumbs", [])),
            paginationNext=PaginationLink.from_dict(item.get("paginationNext", {})),
            paginationPrevious=PaginationLink.from_dict(item.get("paginationPrevious", {})),
        ))

        return super().from_dict(new_item)
