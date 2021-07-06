import sys
from typing import Type, Optional, Tuple, Dict, Callable, Any
from weakref import WeakKeyDictionary

import attr


# Caches the attribute names for attr.s classes
CLASS_ATTRS: WeakKeyDictionary = WeakKeyDictionary()


def split_in_unknown_and_known_fields(data: Optional[dict], item_cls: Type) -> Tuple[Dict, Dict]:
    """
    Return a pair of dicts. The first one contains those elements not belonging to the
    attr class ``item_cls``. The second one contains the rest. That is, those
    attributes not belonging to ``item_cls`` class
    """
    data = data or {}
    if not attr.has(item_cls):
        raise ValueError(f"The cls {item_cls} is not attr.s class")
    if not item_cls in CLASS_ATTRS:
        CLASS_ATTRS[item_cls] = {field.name for field in attr.fields(item_cls)}
    unknown, known = split_dict(data, lambda k: k in CLASS_ATTRS[item_cls])
    return unknown, known


def split_dict(dict: Dict, key_pred: Callable[[Any], Any]) -> Tuple[Dict, Dict]:
    """
    Splits the dictionary in two. The first dict contains the records
    for which the key predicate is False and the second dict contains the rest

    >>> split_dict({}, lambda k: False)
    ({}, {})
    >>> split_dict(dict(a=1, b=2, c=3), lambda k: k != 'a')
    ({'a': 1}, {'b': 2, 'c': 3})
    """
    yes, no = {}, {}
    for k, v in dict.items():
        if key_pred(k):
            yes[k] = v
        else:
            no[k] = v
    return (no, yes)


def export(fn):
    """
    Decorator that includes the decorated element into the
    ``__all__`` variable in the module. Useful to control
    what is imported when ``import * from <module>`` is used.
    """
    mod = sys.modules[fn.__module__]
    if hasattr(mod, '__all__'):
        mod.__all__.append(fn.__name__)
    else:
        mod.__all__ = [fn.__name__]
    return fn