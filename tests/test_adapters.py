from typing import Optional

import attr
import pytest
from itemadapter import ItemAdapter

from autoextract_poet.adapters import AutoExtractAdapter
from autoextract_poet.items import Item


@attr.s(auto_attribs=True, slots=True)
class ItemTest(Item):
    attr1: Optional[int] = attr.ib(default=None, metadata={"meta": "example"})
    attr2: Optional[str] = None


@attr.s(auto_attribs=True, slots=True)
class NonItem:
    attr1: str = "Not extending Item"


@pytest.fixture
def item_adapter():
    ItemAdapter.ADAPTER_CLASSES.appendleft(AutoExtractAdapter)
    yield ItemAdapter
    ItemAdapter.ADAPTER_CLASSES.popleft()


@pytest.fixture
def item() -> AutoExtractAdapter:
    return ItemTest.from_dict(dict(attr1=1,
                                   attr2="regular",
                                   attr3="additional1",
                                   attr4="additional2"))



@pytest.fixture
def adapted_item(item) -> AutoExtractAdapter:
    return AutoExtractAdapter(item)


@pytest.fixture
def empty_item() -> AutoExtractAdapter:
    return AutoExtractAdapter(Item())


def test_is_item():
    assert AutoExtractAdapter.is_item(ItemTest()) is True
    assert AutoExtractAdapter.is_item("Not an item") is False
    assert AutoExtractAdapter.is_item(NonItem()) is False


def test_get_field_meta(adapted_item):
    assert adapted_item.get_field_meta("attr1") == {"meta": "example"}
    assert adapted_item.get_field_meta("attr2") == {}
    assert adapted_item.get_field_meta("attr3") == {}
    assert adapted_item.get_field_meta("anything_else") == {}


def test_field_names(adapted_item):
    expected = ["attr1", "attr2", "attr3", "attr4"]
    assert list(adapted_item.field_names()) == expected
    adapted_item.item._additional_attrs['attr1'] = "duplicated"
    assert list(adapted_item.field_names()) == expected


def test_field_names_on_empty(empty_item):
    assert not empty_item.field_names()
    empty_item.item._additional_attrs['attr'] = "additional"
    assert list(empty_item.field_names()) == ['attr']


def test_getitem_setitem(adapted_item, empty_item):
    assert adapted_item["attr1"] == 1
    assert adapted_item["attr2"] == "regular"
    assert adapted_item["attr3"] == "additional1"
    assert adapted_item["attr4"] == "additional2"

    # Checking that we can set and then get any value. This covers the three
    # cases: attrs attribs, additional attribs and new additional attribs
    for item in [adapted_item, empty_item]:
        for idx in range(1, 6):
            item[f"attr{idx}"] = f"new_{idx}"
        for idx in range(1, 6):
            assert item[f"attr{idx}"] == f"new_{idx}"


def test_delitem(adapted_item):
    del adapted_item["attr1"]
    assert len(adapted_item) == 3
    del adapted_item["attr2"]
    assert len(adapted_item) == 2
    del adapted_item["attr3"]
    assert len(adapted_item) == 1
    del adapted_item["attr4"]
    assert len(adapted_item) == 0

    with pytest.raises(KeyError):
        del adapted_item["attr5"]

    with pytest.raises(KeyError):
        del adapted_item["attr1"]


@pytest.mark.xfail(reason="deleting an attrs makes the object unserialiable with attr")
def test_serialization_after_deletion(adapted_item):
    del adapted_item["attr1"]
    assert len(attr.asdict(adapted_item.item)) == 3


def test_iter(adapted_item, empty_item):
    assert list(empty_item) == []
    assert list(adapted_item) == [f"attr{idx}" for idx in range(1, 5)]
    del adapted_item["attr1"]
    assert list(adapted_item) == [f"attr{idx}" for idx in range(2, 5)]
    del adapted_item["attr4"]
    assert list(adapted_item) == [f"attr{idx}" for idx in range(2, 4)]


def test_asdict(item_adapter, item):
    # Order is important
    expected = list(dict(attr1=1,
                    attr2="regular",
                    attr3="additional1",
                    attr4="additional2").items())
    adapted_item = item_adapter(item)
    assert list(adapted_item.asdict().items()) == expected

    # Items should be serializable after attr.s attributes removal
    del adapted_item["attr1"]
    assert list(adapted_item.asdict().items()) == [("attr2", "regular"),
                                                   ("attr3", "additional1"),
                                                   ("attr4", "additional2")]
