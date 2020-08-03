import json
import os

from autoextract_poet.items import (
    AdditionalProperty,
    Breadcrumb,
    Item,
    GTIN,
    Offer,
    Rating,
)


def load_fixture(name):
    path = os.path.join(
        os.path.dirname(__file__),
        f"fixtures/{name}"
    )
    with open(path, 'r') as f:
        return json.loads(f.read())


def compare_item_with_dict(item: Item, data: dict):
    """Compare an Item with the dict that could have originated it.

    Return True if they're equivalent or False otherwise.
    """
    for key, value in data.items():
        if key == 'additionalProperty':
            value = AdditionalProperty.from_list(value)
        if key == 'aggregateRating':
            value = Rating.from_dict(value)
        if key == 'breadcrumbs':
            value = Breadcrumb.from_list(value)
        if key == 'gtin':
            value = GTIN.from_list(value)
        if key == 'offers':
            value = Offer.from_list(value)

        if getattr(item, key) != value:
            return False

    return True
