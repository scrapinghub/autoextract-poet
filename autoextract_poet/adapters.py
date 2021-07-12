from types import MappingProxyType
from typing import Any, KeysView, Iterator

from itemadapter.adapter import AttrsAdapter

from autoextract_poet.items import Item


class AutoExtractAdapter(AttrsAdapter):
    """
    ``ItemAdapter`` for AutoExtract poet items. The advantage of
    this adapter over the default one is that any new attributes
    no present in the item definition are also preserved and serialized.
    This ensures compatibility with the addition of new attributes
    in the AutoExtract API.

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
