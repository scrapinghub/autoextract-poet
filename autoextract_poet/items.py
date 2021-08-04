from typing import Dict, List, Optional

import attr

from .util import split_in_unknown_and_known_fields


class _ItemBase:
    # Reserving an slot for _unknown_fields_dict.
    # This is done in a base class because otherwise attr.s won't pick it up
    __slots__ = ("_unknown_fields_dict", )


@attr.s(auto_attribs=True, slots=True)
class Item(_ItemBase):

    def __attrs_post_init__(self):
        self._unknown_fields_dict = {}

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        """
        Read an item from a dictionary.

        Unknown attributes are kept in the dict ``_unknown_fields_dict``
        so that ``AutoExtractAdapter`` can include them in the resultant item.
        This ensures supporting new AutoExtract fields even if the
        item library is not in sync.
        """
        if not item:
            return None
        unknown_fields, known_fields = split_in_unknown_and_known_fields(item, cls)
        obj = cls(**known_fields)  # type: ignore
        obj._unknown_fields_dict = unknown_fields
        return obj

    @classmethod
    def from_list(cls, items: Optional[List[Dict]]) -> List:
        """
        Read items from a list, invoking ``from_dict`` for each item in the list
        """
        return [cls.from_dict(item) for item in items or []]


def _apply_types(item: Optional[dict], *,
                 from_dict: dict = None,
                 from_list: dict = None) -> Optional[dict]:
    """
    Utility function to wrap basic types into data structures.

    Assumptions:
    * field names stay the same;
    * from_dict fields are optional, and in case of an absent field
      we're preserving None instead of creating an empty data structure;
    * from_list fields are optional, but in case of an absent field
      an empty list is created.
    """
    if not item:
        return None

    new_item = dict(**item)
    new_item.update({
        key: cls.from_dict(item.get(key))
        for key, cls in (from_dict or {}).items()
    })
    new_item.update({
        key: cls.from_list(item.get(key, []))
        for key, cls in (from_list or {}).items()
    })
    return new_item


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
class PaginationLink(Item):

    url: Optional[str] = None
    text: Optional[str] = None


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
        new_item = _apply_types(item, from_list={'breadcrumbs': Breadcrumb})
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class ArticleFromList(Item):

    url: Optional[str] = None
    probability: Optional[float] = None
    headline: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    author: Optional[str] = None
    authorsList: List[str] = attr.Factory(list)
    inLanguage: Optional[str] = None
    mainImage: Optional[str] = None
    images: List[str] = attr.Factory(list)
    articleBody: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class ArticleList(Item):

    url: Optional[str] = None
    articles: List[ArticleFromList] = attr.Factory(list)
    paginationNext: Optional[PaginationLink] = None
    paginationPrevious: Optional[PaginationLink] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(
            item,
            from_list={'articles': ArticleFromList},
            from_dict={
                'paginationNext': PaginationLink,
                'paginationPrevious': PaginationLink
            }
        )
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class Product(Item):

    url: Optional[str] = None
    canonicalUrl: Optional[str] = None
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
    descriptionHtml: Optional[str] = None
    additionalProperty: List[AdditionalProperty] = attr.Factory(list)
    aggregateRating: Optional[Rating] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(
            item,
            from_dict={'aggregateRating': Rating},
            from_list={
                'additionalProperty': AdditionalProperty,
                'breadcrumbs': Breadcrumb,
                'gtin': GTIN,
                'offers': Offer,
            }
        )
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
        new_item = _apply_types(
            item,
            from_dict={'aggregateRating': Rating},
            from_list={'offers': Offer}
        )
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class ProductList(Item):

    url: Optional[str] = None
    products: List[ProductFromList] = attr.Factory(list)
    breadcrumbs: List[Breadcrumb] = attr.Factory(list)
    paginationNext: Optional[PaginationLink] = None
    paginationPrevious: Optional[PaginationLink] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(
            item,
            from_list={
                'products': ProductFromList,
                'breadcrumbs': Breadcrumb,
            },
            from_dict={
                'paginationNext': PaginationLink,
                'paginationPrevious': PaginationLink,
            }
        )
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class Location(Item):

    raw: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Organization(Item):

    raw: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Salary(Item):
    raw: Optional[str] = None
    value: Optional[float] = None
    currency: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class JobPosting(Item):

    probability: Optional[float] = None
    url: Optional[str] = None
    title: Optional[str] = None
    datePosted: Optional[str] = None
    validThrough: Optional[str] = None
    description: Optional[str] = None
    descriptionHtml: Optional[str] = None
    employmentType: Optional[str] = None
    hiringOrganization: Optional[Organization] = None
    baseSalary: Optional[Salary] = None
    jobLocation: Optional[Location] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(item, from_dict={
            "hiringOrganization": Organization,
            "baseSalary": Salary,
            "jobLocation": Location,
        })
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class Comment(Item):

    probability: Optional[float] = None
    text: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    upvoteCount: Optional[int] = None
    downvoteCount: Optional[int] = None


@attr.s(auto_attribs=True, slots=True)
class Comments(Item):

    url: Optional[str] = None
    comments: List[Comment] = attr.Factory(list)

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(item, from_list={"comments": Comment})
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class ForumPost(Item):

    probability: Optional[float] = None
    text: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    upvoteCount: Optional[int] = None
    downvoteCount: Optional[int] = None
    replyCount: Optional[int] = None


@attr.s(auto_attribs=True, slots=True)
class Topic(Item):

    name: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class ForumPosts(Item):

    url: Optional[str] = None
    topic: Optional[Topic] = None
    posts: List[ForumPost] = attr.Factory(list)

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(item,
                                from_list={"posts": ForumPost},
                                from_dict={"topic": Topic})
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class Address(Item):

    postalCode: Optional[str] = None
    streetAddress: Optional[str] = None
    addressCountry: Optional[str] = None
    addressLocality: Optional[str] = None
    addressRegion: Optional[str] = None
    raw: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Area(Item):

    value: Optional[float] = None
    unitCode: Optional[str] = None
    raw: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class TradeAction(Item):

    tradeType: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class RealEstate(Item):

    url: Optional[str] = None
    probability: Optional[float] = None
    name: Optional[str] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    description: Optional[str] = None
    mainImage: Optional[str] = None
    images: List[str] = attr.Factory(list)
    yearBuilt: Optional[int] = None
    breadcrumbs: List[Breadcrumb] = attr.Factory(list)
    additionalProperty: List[AdditionalProperty] = attr.Factory(list)
    address: Optional[Address] = None
    area: Optional[Area] = None
    numberOfBathroomsTotal: Optional[int] = None
    numberOfFullBathrooms: Optional[int] = None
    numberOfPartialBathrooms: Optional[int] = None
    numberOfBedrooms: Optional[int] = None
    numberOfRooms: Optional[int] = None
    identifier: Optional[str] = None
    tradeActions: List[TradeAction] = attr.Factory(list)

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(
            item,
            from_list={
                "additionalProperty": AdditionalProperty,
                "breadcrumbs": Breadcrumb,
                "tradeActions": TradeAction
            },
            from_dict={
                "address": Address,
                "area": Area,
            }
        )
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class Review(Item):
    
    name: Optional[str] = None
    reviewBody: Optional[str] = None
    reviewRating: Optional[Rating] = None
    datePublished: Optional[str] = None
    datePublishedRaw: Optional[str] = None
    votedHelpful: Optional[int] = None
    votedUnhelpful: Optional[int] = None
    isVerified: Optional[bool] = None
    probability: Optional[float] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(item, from_dict={"reviewRating": Rating})
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class Reviews(Item):

    url: Optional[str] = None
    reviews: List[Review] = attr.Factory(list)
    paginationNext: Optional[PaginationLink] = None
    paginationPrevious: Optional[PaginationLink] = None

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(
            item,
            from_list={
                'reviews': Review,
            },
            from_dict={
                'paginationNext': PaginationLink,
                'paginationPrevious': PaginationLink,
            }
        )
        return super().from_dict(new_item)


@attr.s(auto_attribs=True, slots=True)
class MileageFromOdometer(Item):

    value: Optional[int] = None
    unitCode: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class VehicleEngine(Item):

    raw: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class AvailableAtOrFrom(Item):

    raw: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class FuelEfficiency(Item):

    raw: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class Vehicle(Item):

    url: Optional[str] = None
    canonicalUrl: Optional[str] = None
    probability: Optional[float] = None
    name: Optional[str] = None
    offers: List[Offer] = attr.Factory(list)
    sku: Optional[str] = None
    mpn: Optional[str] = None
    brand: Optional[str] = None
    breadcrumbs: List[Breadcrumb] = attr.Factory(list)
    mainImage: Optional[str] = None
    images: List[str] = attr.Factory(list)
    description: Optional[str] = None
    descriptionHtml: Optional[str] = None
    additionalProperty: List[AdditionalProperty] = attr.Factory(list)
    aggregateRating: Optional[Rating] = None
    vehicleIdentificationNumber: Optional[str] = None
    mileageFromOdometer: Optional[MileageFromOdometer] = None
    vehicleTransmission: Optional[str] = None
    fuelType: Optional[str] = None
    vehicleEngine: Optional[VehicleEngine] = None
    color: Optional[str] = None
    vehicleInteriorColor: Optional[str] = None
    availableAtOrFrom: Optional[AvailableAtOrFrom] = None
    numberOfDoors: Optional[int] = None
    vehicleSeatingCapacity: Optional[int] = None
    fuelEfficiency: List[FuelEfficiency] = attr.Factory(list)

    @classmethod
    def from_dict(cls, item: Optional[Dict]):
        new_item = _apply_types(
            item,
            from_dict={
                'aggregateRating': Rating,
                'mileageFromOdometer': MileageFromOdometer,
                'vehicleEngine': VehicleEngine,
                'availableAtOrFrom': AvailableAtOrFrom,
            },
            from_list={
                'additionalProperty': AdditionalProperty,
                'breadcrumbs': Breadcrumb,
                'offers': Offer,
                'fuelEfficiency': FuelEfficiency,
            }
        )
        return super().from_dict(new_item)
