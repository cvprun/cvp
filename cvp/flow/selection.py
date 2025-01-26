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

from cvp.flow.arc import FlowArc
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.memory.variable import Variable
from cvp.types.shapes import Point

FlowSelectableKey: TypeAlias = int
FlowSelectableAny = Union[FlowNode, FlowPin, FlowArc, Variable]
FlowSelectableDict = OrderedDict[FlowSelectableKey, FlowSelectableAny]


class FlowSelection:
    _items: FlowSelectableDict

    def __init__(self, items: Optional[FlowSelectableDict] = None):
        self._items = items if items else FlowSelectableDict()

    def __len__(self) -> int:
        return self._items.__len__()

    def __contains__(self, item: Union[FlowSelectableKey, FlowSelectableAny]) -> bool:
        if not isinstance(item, FlowSelectableKey):
            item = id(item)

        assert isinstance(item, FlowSelectableKey)
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
    def _is_node(item: FlowSelectableAny) -> TypeGuard[FlowNode]:
        return isinstance(item, FlowNode)

    @staticmethod
    def _is_pin(item: FlowSelectableAny) -> TypeGuard[FlowPin]:
        return isinstance(item, FlowPin)

    @staticmethod
    def _is_arc(item: FlowSelectableAny) -> TypeGuard[FlowArc]:
        return isinstance(item, FlowArc)

    @staticmethod
    def _is_variable(item: FlowSelectableAny) -> TypeGuard[Variable]:
        return isinstance(item, Variable)

    @property
    def nodes(self) -> List[FlowNode]:
        return list(filter(self._is_node, self._items.values()))

    @property
    def pins(self) -> List[FlowPin]:
        return list(filter(self._is_pin, self._items.values()))

    @property
    def arcs(self) -> List[FlowArc]:
        return list(filter(self._is_arc, self._items.values()))

    @property
    def variables(self) -> List[Variable]:
        return list(filter(self._is_variable, self._items.values()))

    @property
    def first(self) -> FlowSelectableAny:
        return next(iter(self._items.values()))

    @property
    def last(self) -> FlowSelectableAny:
        return next(reversed(self._items.values()))

    @property
    def selected_node_only(self) -> Optional[FlowNode]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, FlowNode) else None

    @property
    def selected_pin_only(self) -> Optional[FlowPin]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, FlowPin) else None

    @property
    def selected_arc_only(self) -> Optional[FlowArc]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, FlowArc) else None

    @property
    def selected_variable_only(self) -> Optional[Variable]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, Variable) else None

    def clear(self) -> None:
        self._items.clear()

    def extends(self, items: Iterable[FlowSelectableAny]) -> None:
        for item in items:
            self._items[id(item)] = item

    def add(self, item: FlowSelectableAny) -> None:
        self._items[id(item)] = item

    def remove(self, item: FlowSelectableAny) -> None:
        self._items.pop(id(item))

    def remove_noraise(self, item: FlowSelectableAny) -> None:
        try:
            self.remove(item)
        except KeyError:
            pass

    def apply(self, item: FlowSelectableAny) -> None:
        if item.selected:
            self.add(item)
        else:
            self.remove_noraise(item)

    @property
    def group_pos(self) -> Point:
        x = min([node.x1 for node in self.nodes])
        y = min([node.y1 for node in self.nodes])
        return x, y

    def copy_validated_items(
        self,
        point: Point,
    ) -> Tuple[List[FlowNode], List[FlowArc], List[Variable]]:
        nodes = self.nodes
        arcs = self.arcs
        variables = self.variables
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
                        candidate_arc.input = FlowNodePin(new_node, input_pin)

                if candidate_arc.output is None:
                    if output_pin := new_node.find_output_pin(candidate_arc.uuid):
                        candidate_arc.output = FlowNodePin(new_node, output_pin)

            if candidate_arc.input and candidate_arc.output:
                new_arcs.append(candidate_arc)

        new_variables = [deepcopy(variable) for variable in variables]

        return new_nodes, new_arcs, new_variables
