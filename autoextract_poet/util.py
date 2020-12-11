from typing import Type, Optional
from weakref import WeakKeyDictionary

import attr


# Caches the attribute names for attr.s classes
CLASS_ATTRS: WeakKeyDictionary = WeakKeyDictionary()


def remove_unknown_fields(data: Optional[dict], item_cls: Type) -> dict:
    """Return a dict where those elements not belonging to the
    attr class ``item_cls`` definition are removed. This dict is then safe to
    be used to create items for the given class. Can be used to ensure
    that new attributes returned from the API does not break the library"""
    data = data or {}
    if not attr.has(item_cls):
        raise ValueError(f"The cls {item_cls} is not attr.s class")

    if not item_cls in CLASS_ATTRS:
        CLASS_ATTRS[item_cls] = {field.name for field in attr.fields(item_cls)}
    return {k: v for k, v in data.items() if k in CLASS_ATTRS[item_cls]}