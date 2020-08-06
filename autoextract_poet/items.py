from typing import List, Optional

import attr


@attr.s(auto_attribs=True, slots=True)
class Item:

    @classmethod
    def from_dict(cls, item: dict):
        return cls(**item)  # type: ignore

    @classmethod
    def _get_attr_cls(cls, annotation):
        """Inspect type annotation searching for a subclass of Item"""
        if type(annotation) is type:
            # Annotation is a class/type
            return annotation if issubclass(annotation, Item) else None

        # Annotation is probably a typing instance
        for arg in annotation.__args__:
            attr_cls = cls._get_attr_cls(arg)
            if attr_cls:
                return attr_cls

    def __attrs_post_init__(self):
        for attribute in self.__attrs_attrs__:
            annotation = self.__annotations__.get(attribute.name)
            attr_cls = self._get_attr_cls(annotation)
            if not attr_cls:
                # Annotation does not mention an Item subclass
                continue

            def get_new_value(value):
                if isinstance(value, dict):
                    # We can build an instance from a dict
                    return attr_cls.from_dict(value)
                else:
                    # Nothing to do here
                    return value

            value = getattr(self, attribute.name, None)
            if isinstance(value, (list, tuple, )):
                new_value = list(map(get_new_value, value))
            else:
                new_value = get_new_value(value)

            setattr(self, attribute.name, new_value)


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
