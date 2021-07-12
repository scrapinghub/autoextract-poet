from types import MappingProxyType
from typing import Any, KeysView, Iterator

from itemadapter.adapter import AttrsAdapter

from autoextract_poet.items import Item


class AutoExtractAdapter(AttrsAdapter):
    """
    ``ItemAdapter`` for AutoExtract poet items that deals transparently with
    both the ``attr.s`` defined fields and the rest of unknown
    fields received at item initialization, offering an unified view over
    all the item fields.

    The utility is twofold. Firstly, it serves to ensure the
    pass-through of new fields from the API even if ``autoextract-poet``
    item definitions have not been yet updated. In other words,
    it can be used to create spiders that preserve all the data coming
    from the API even if they don't have updated item definitions.

    Secondly, it offers a common interface to access and modify both kind of
    fields (known and unknown).

    Remember that this adapter should be enabled by invoking::

        ItemAdapter.ADAPTER_CLASSES.appendleft(AutoExtractAdapter)
    """
    def __init__(self, item: Any) -> None:
        super().__init__(item)

    @classmethod
    def is_item(cls, item: Any) -> bool:
        return isinstance(item, Item)

    def get_field_meta(self, field_name: str) -> MappingProxyType:
        if field_name in self._fields_dict:
            return self._fields_dict[field_name].metadata  # type: ignore
        else:
            return MappingProxyType({})

    def field_names(self) -> KeysView:
        return KeysView({**self._fields_dict, **self.item._unknown_fields_dict})

    def __getitem__(self, field_name: str) -> Any:
        if field_name in self._fields_dict:
            return getattr(self.item, field_name)
        elif field_name in self.item._unknown_fields_dict:
            return self.item._unknown_fields_dict[field_name]
        raise KeyError(field_name)

    def __setitem__(self, field_name: str, value: Any) -> None:
        if field_name in self._fields_dict:
            setattr(self.item, field_name, value)
        else:
            self.item._unknown_fields_dict[field_name] = value

    def __delitem__(self, field_name: str) -> None:
        if field_name in self._fields_dict:
            try:
                delattr(self.item, field_name)
            except AttributeError:
                raise KeyError(field_name)
        elif field_name in self.item._unknown_fields_dict:
            del self.item._unknown_fields_dict[field_name]
        else:
            raise KeyError(f"Object of type {self.item.__class__.__name__} does " +
                           f"not contain a field with name {field_name}")

    def __iter__(self) -> Iterator:
        fields = [attr for attr in self._fields_dict if hasattr(self.item, attr)]
        fields.extend(attr for attr in self.item._unknown_fields_dict if attr not in fields)
        return iter(fields)
