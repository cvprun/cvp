# -*- coding: utf-8 -*-

from collections import OrderedDict
from copy import copy, deepcopy
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeAlias,
    TypeGuard,
    Union,
)
from uuid import uuid4

from cvp.flow.datas.arc import Arc
from cvp.flow.datas.node import Node
from cvp.flow.datas.node_pin import NodePin
from cvp.flow.datas.pin import Pin
from cvp.types.shapes import Point

SelectableKey: TypeAlias = int
SelectableAny = Union[Node, Pin, Arc]
SelectableDict = OrderedDict[SelectableKey, SelectableAny]


class Selection:
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

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result._items = copy(self._items)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result._items = deepcopy(self._items, memo)
        memo[id(self)] = result
        return result

    def copy(self):
        return self.__copy__()

    def deepcopy(self):
        return self.__deepcopy__()

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
        first = self.first
        return first if isinstance(first, Pin) else None

    @property
    def selected_arc_only(self) -> Optional[Arc]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, Arc) else None

    def clear(self) -> None:
        self._items.clear()

    def extends(self, items: Iterable[SelectableAny]) -> None:
        for item in items:
            self._items[id(item)] = item

    def add(self, item: SelectableAny) -> None:
        self._items[id(item)] = item

    def remove(self, item: SelectableAny) -> None:
        self._items.pop(id(item))

    def remove_noraise(self, item: SelectableAny) -> None:
        try:
            self.remove(item)
        except KeyError:
            pass

    def apply(self, item: SelectableAny) -> None:
        if item.selected:
            self.add(item)
        else:
            self.remove_noraise(item)

    @property
    def group_pos(self) -> Point:
        x = min([node.x1 for node in self.nodes])
        y = min([node.y1 for node in self.nodes])
        return x, y

    def copy_validated_items(self, point: Point) -> Tuple[List[Node], List[Arc]]:
        nodes = self.nodes
        arcs = self.arcs
        dx, dy = self.group_pos
        x = point[0] - dx
        y = point[1] - dy

        new_nodes = list()
        candidate_arcs = list()
        arc_uuid_mapping = {arc.uuid: str(uuid4()) for arc in arcs}

        for arc in arcs:
            arc = deepcopy(arc)
            arc.uuid = arc_uuid_mapping[arc.uuid]
            arc.output = None
            arc.input = None
            arc.polyline.clear()
            candidate_arcs.append(arc)

        for node in nodes:
            node = deepcopy(node)
            node.uuid = str(uuid4())
            nx, ny = node.node_pos
            node.node_pos = x + nx, y + ny
            new_nodes.append(node)

            # Remap old_arc_uuid to new_arc_uuid
            for pin in node.pins:
                for i, old_arc_uuid in enumerate(pin.arcs):
                    if old_arc_uuid in arc_uuid_mapping:
                        pin.arcs[i] = arc_uuid_mapping[old_arc_uuid]

        new_arcs = list()

        # Connect the arc to a pin on the local node.
        for candidate_arc in candidate_arcs:
            assert candidate_arc.input is None
            assert candidate_arc.output is None

            for new_node in new_nodes:
                if candidate_arc.input is None:
                    if input_pin := new_node.find_input_pin(candidate_arc.uuid):
                        candidate_arc.input = NodePin(new_node, input_pin)

                if candidate_arc.output is None:
                    if output_pin := new_node.find_output_pin(candidate_arc.uuid):
                        candidate_arc.output = NodePin(new_node, output_pin)

            if candidate_arc.input and candidate_arc.output:
                new_arcs.append(candidate_arc)

        return new_nodes, new_arcs
