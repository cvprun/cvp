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

from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.flow.variable import FlowVariable
from cvp.flow.wire import FlowWire
from cvp.types.shapes import Point

FlowSelectableKey: TypeAlias = int
FlowSelectableAny = Union[FlowNode, FlowPin, FlowWire, FlowVariable]
FlowSelectableDict = OrderedDict[FlowSelectableKey, FlowSelectableAny]


class FlowSelection:
    _items: FlowSelectableDict

    def __init__(self, items: Optional[FlowSelectableDict] = None):
        self._items = items if items else FlowSelectableDict()

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._items == other._items

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
    def _is_wire(item: FlowSelectableAny) -> TypeGuard[FlowWire]:
        return isinstance(item, FlowWire)

    @staticmethod
    def _is_variable(item: FlowSelectableAny) -> TypeGuard[FlowVariable]:
        return isinstance(item, FlowVariable)

    @property
    def nodes(self) -> List[FlowNode]:
        return list(filter(self._is_node, self._items.values()))

    @property
    def pins(self) -> List[FlowPin]:
        return list(filter(self._is_pin, self._items.values()))

    @property
    def wires(self) -> List[FlowWire]:
        return list(filter(self._is_wire, self._items.values()))

    @property
    def variables(self) -> List[FlowVariable]:
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
    def selected_wire_only(self) -> Optional[FlowWire]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, FlowWire) else None

    @property
    def selected_variable_only(self) -> Optional[FlowVariable]:
        if 1 != len(self._items):
            return None
        first = self.first
        return first if isinstance(first, FlowVariable) else None

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
    ) -> Tuple[List[FlowNode], List[FlowWire], List[FlowVariable]]:
        nodes = self.nodes
        wires = self.wires
        variables = self.variables
        dx, dy = self.group_pos
        x = point[0] - dx
        y = point[1] - dy

        new_nodes = list()
        candidate_wires = list()
        wire_uuid_mapping = {wire.uuid: str(uuid4()) for wire in wires}

        for wire in wires:
            wire = deepcopy(wire)
            wire.uuid = wire_uuid_mapping[wire.uuid]
            wire.output = None
            wire.input = None
            wire.polyline.clear()
            candidate_wires.append(wire)

        for node in nodes:
            node = deepcopy(node)
            node.uuid = str(uuid4())
            nx, ny = node.node_pos
            node.node_pos = x + nx, y + ny
            new_nodes.append(node)

            # Remap old_wire_uuid to new_wire_uuid
            for pin in node.pins:
                for i, old_wire_uuid in enumerate(pin.wires):
                    if old_wire_uuid in wire_uuid_mapping:
                        pin.wires[i] = wire_uuid_mapping[old_wire_uuid]

        new_wires = list()

        # Connect the wire to a pin on the local node.
        for candidate_wire in candidate_wires:
            assert candidate_wire.input is None
            assert candidate_wire.output is None

            for new_node in new_nodes:
                if candidate_wire.input is None:
                    if input_pin := new_node.find_input_pin(candidate_wire.uuid):
                        candidate_wire.input = FlowNodePin(new_node, input_pin)

                if candidate_wire.output is None:
                    if output_pin := new_node.find_output_pin(candidate_wire.uuid):
                        candidate_wire.output = FlowNodePin(new_node, output_pin)

            if candidate_wire.input and candidate_wire.output:
                new_wires.append(candidate_wire)

        new_variables = [deepcopy(variable) for variable in variables]

        return new_nodes, new_wires, new_variables
