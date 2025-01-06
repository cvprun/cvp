# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Iterable, List, Optional, TypeAlias, TypeGuard, Union

from cvp.flow.datas.arc import Arc
from cvp.flow.datas.node import Node
from cvp.flow.datas.pin import Pin

SelectableKey: TypeAlias = int
SelectableAny = Union[Node, Pin, Arc]
SelectableDict = OrderedDict[SelectableKey, SelectableAny]


class SelectedItems:
    _items: SelectableDict

    def __init__(self, items: Optional[SelectableDict] = None):
        self._items = items if items else SelectableDict()

    def __len__(self) -> int:
        return self._items.__len__()

    def __contains__(self, item: Union[SelectableKey, SelectableAny]) -> bool:
        if not isinstance(item, SelectableKey):
            item = id(item)

        assert isinstance(item, SelectableKey)
        return self._items.__contains__(item)

    def __bool__(self):
        return bool(self._items)

    def keys(self):
        return self._items.keys()

    def values(self):
        return self._items.values()

    def items(self):
        return self._items.items()

    def copy(self):
        return self.__class__(self._items.copy())

    @staticmethod
    def _is_node(item: SelectableAny) -> TypeGuard[Node]:
        return isinstance(item, Node)

    @staticmethod
    def _is_pin(item: SelectableAny) -> TypeGuard[Pin]:
        return isinstance(item, Pin)

    @staticmethod
    def _is_arc(item: SelectableAny) -> TypeGuard[Arc]:
        return isinstance(item, Arc)

    @property
    def nodes(self) -> List[Node]:
        return list(filter(self._is_node, self._items.values()))

    @property
    def pins(self) -> List[Pin]:
        return list(filter(self._is_pin, self._items.values()))

    @property
    def arcs(self) -> List[Arc]:
        return list(filter(self._is_arc, self._items.values()))

    @property
    def first(self) -> SelectableAny:
        return next(iter(self._items.values()))

    @property
    def last(self) -> SelectableAny:
        return next(reversed(self._items.values()))

    @property
    def selected_node_only(self) -> Optional[Node]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, Node) else None

    @property
    def selected_pin_only(self) -> Optional[Pin]:
        if 1 != len(self._items):
            return None
        first_item = next(iter(self._items.values()))
        if isinstance(first_item, Pin):
            return first_item
        else:
            return None

    @property
    def selected_arc_only(self) -> Optional[Arc]:
        if 1 != len(self._items):
            return None
        first_item = next(iter(self._items.values()))
        if isinstance(first_item, Arc):
            return first_item
        else:
            return None

    def clear(self) -> None:
        self._items.clear()

    def extends(self, items: Iterable[SelectableAny]) -> None:
        for item in items:
            self._items[id(item)] = item

    def add(self, item: SelectableAny) -> None:
        if not item.selected:
            raise ValueError("Item must be selected")

        self._items[id(item)] = item

    def remove_noraise(self, item: SelectableAny) -> None:
        try:
            self._items.pop(id(item))
        except KeyError:
            pass

    def remove(self, item: SelectableAny) -> None:
        if item.selected:
            raise ValueError("Items must be unselected")

        try:
            self._items.pop(id(item))
        except KeyError:
            pass

    def apply(self, item: SelectableAny) -> None:
        if item.selected:
            self.add(item)
        else:
            self.remove(item)
