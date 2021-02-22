import attr
import pytest

from autoextract_poet.util import remove_unknown_fields


@attr.s(auto_attribs=True)
class _TestItem:
    k1: int
    k2: int


def test_remove_unknown_fields():
    expected = dict(k1=1, k2=2)
    prep1 = remove_unknown_fields(dict(k1=1, k2=2, extra=3), _TestItem)
    prep2 = remove_unknown_fields(dict(k1=1, k2=2, extra=3), _TestItem)
    assert prep1 == prep2
    assert prep2 == expected
    assert attr.asdict(_TestItem(**prep2)) == expected

    with pytest.raises(ValueError):
        remove_unknown_fields(expected, str)