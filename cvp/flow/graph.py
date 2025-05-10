# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from functools import reduce
from math import sqrt
from typing import Any, Dict, Iterable, List, NewType, Optional, Set, Union
from uuid import uuid4

import shapely
from type_serialize import Serializable, deserialize, serialize

from cvp.canvas.control import ViewControl
from cvp.canvas.options import DrawingOptions
from cvp.containers.mapping_deque import MappingDeque
from cvp.dtypes.dtype import Dtype
from cvp.flow.anchor import FlowAnchor
from cvp.flow.connection import FlowConnection
from cvp.flow.history import FlowHistory
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.flow.selection import FlowSelectableAny, FlowSelection
from cvp.flow.variable import FlowVariable, VariableKey
from cvp.flow.wire import FlowWire
from cvp.fonts.types import IconCode
from cvp.logging.logging import flow_logger as logger
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override
from cvp.types.shapes import Point, Size

GraphKey = NewType("GraphKey", str)


class FlowGraph(Serializable):

    @unique
    class _Keys(StrEnum):
        uuid = auto()
        name_ = "name"
        docs = auto()
        icon = auto()
        lock = auto()
        opened = auto()
        color = auto()
        nodes = auto()
        wires = auto()
        variables = auto()
        control = auto()
        options = auto()
        tags = auto()

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[IconCode] = None,
        lock=False,
        opened=False,
        color: RGBA = WHITE_RGBA,
        nodes: Optional[Iterable[FlowNode]] = None,
        wires: Optional[Iterable[FlowWire]] = None,
        variables: Optional[Iterable[FlowVariable]] = None,
        control: Optional[ViewControl] = None,
        options: Optional[DrawingOptions] = None,
        tags: Optional[Iterable[str]] = None,
        *,
        selection: Optional[FlowSelection] = None,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.docs = docs if docs else str()
        self.icon = icon if icon else IconCode(str())
        self.lock = lock
        self.opened = opened
        self.color = color
        self.nodes = self.__create_nodes(nodes)
        self.wires = self.__create_wires(wires)
        self.variables = self.__create_variables(variables)
        self.control = control if control else ViewControl()
        self.options = options if options else DrawingOptions()
        self.tags = list(tags if tags else ())
        self._selection = selection if selection else FlowSelection()

        self._history = FlowHistory(max_history=self.options.max_history)
        self._history.save_history("Initialize graph", self)

    @staticmethod
    def __node_keyable(node: FlowNode) -> str:
        return node.uuid

    @staticmethod
    def __wire_keyable(wire: FlowWire) -> str:
        return wire.uuid

    @staticmethod
    def __variable_keyable(variable: FlowVariable) -> str:
        return variable.key

    def __create_nodes(self, nodes: Optional[Iterable[FlowNode]] = None):
        return MappingDeque[str, FlowNode](items=nodes, keyable=self.__node_keyable)

    def __create_wires(self, wires: Optional[Iterable[FlowWire]] = None):
        return MappingDeque[str, FlowWire](items=wires, keyable=self.__wire_keyable)

    def __create_variables(self, variables: Optional[Iterable[FlowVariable]] = None):
        return MappingDeque[str, FlowVariable](
            items=variables,
            keyable=self.__variable_keyable,
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.uuid == other.uuid
            and self.name == other.name
            and self.docs == other.docs
            and self.icon == other.icon
            and self.lock == other.lock
            and self.opened == other.opened
            and self.color == other.color
            and self.nodes == other.nodes
            and self.wires == other.wires
            and self.variables == other.variables
            and self.control == other.control
            and self.options == other.options
            and self.tags == other.tags
        )

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = copy(self.uuid)
        result.name = copy(self.name)
        result.docs = copy(self.docs)
        result.icon = copy(self.icon)
        result.lock = copy(self.lock)
        result.opened = copy(self.opened)
        result.color = copy(self.color)
        result.nodes = copy(self.nodes)
        result.wires = copy(self.wires)
        result.variables = copy(self.variables)
        result.control = copy(self.control)
        result.options = copy(self.options)
        result.tags = copy(self.tags)
        result._selection = copy(self._selection)
        result._history = copy(self._history)
        return result

    def __deepcopy__(self, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        cls = self.__class__
        result = cls.__new__(cls)
        result.uuid = deepcopy(self.uuid, memo)
        result.name = deepcopy(self.name, memo)
        result.docs = deepcopy(self.docs, memo)
        result.icon = deepcopy(self.icon, memo)
        result.lock = deepcopy(self.lock, memo)
        result.opened = deepcopy(self.opened, memo)
        result.color = deepcopy(self.color, memo)
        result.nodes = deepcopy(self.nodes, memo)
        result.wires = deepcopy(self.wires, memo)
        result.variables = deepcopy(self.variables, memo)
        result.control = deepcopy(self.control, memo)
        result.options = deepcopy(self.options, memo)
        result.tags = deepcopy(self.tags, memo)
        result._selection = deepcopy(self._selection, memo)
        result._history = deepcopy(self._history, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        return {
            str(self._Keys.uuid): str(self.uuid),
            str(self._Keys.name_): str(self.name),
            str(self._Keys.docs): str(self.docs),
            str(self._Keys.icon): str(self.icon),
            str(self._Keys.lock): bool(self.lock),
            str(self._Keys.opened): bool(self.opened),
            str(self._Keys.color): list(float(c) for c in self.color),
            str(self._Keys.nodes): serialize(self.nodes.as_list()),
            str(self._Keys.wires): serialize(self.wires.as_list()),
            str(self._Keys.variables): serialize(self.variables.as_list()),
            str(self._Keys.control): serialize(self.control),
            str(self._Keys.options): serialize(self.options),
            str(self._Keys.tags): list(str(t) for t in self.tags),
        }

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = str(data.get(self._Keys.uuid, str()))
        self.name = str(data.get(self._Keys.name_, str()))
        self.docs = str(data.get(self._Keys.docs, str()))
        self.icon = IconCode(data.get(self._Keys.icon, str()))
        self.lock = bool(data.get(self._Keys.lock, False))
        self.opened = bool(data.get(self._Keys.opened, False))
        self.color = tuple(data.get(self._Keys.color, WHITE_RGBA))

        assert len(self.color) == 4
        assert all(isinstance(c, float) for c in self.color)

        nodes = list()
        wires = list()
        variables = list()

        if raw_nodes := data.get(self._Keys.nodes):
            for raw_node in raw_nodes:
                nodes.append(deserialize(raw_node, FlowNode))

        if raw_wires := data.get(self._Keys.wires):
            for raw_wire in raw_wires:
                wires.append(deserialize(raw_wire, FlowWire))

        if raw_variables := data.get(self._Keys.variables):
            for raw_variable in raw_variables:
                variables.append(deserialize(raw_variable, FlowVariable))

        self.nodes = self.__create_nodes(nodes)
        self.wires = self.__create_wires(wires)
        self.variables = self.__create_variables(variables)

        if control := data.get(self._Keys.control):
            self.control = deserialize(control, ViewControl)
        else:
            self.control = ViewControl()

        if options := data.get(self._Keys.options):
            self.options = deserialize(options, DrawingOptions)
        else:
            self.options = DrawingOptions()

        self.tags = data.get(self._Keys.tags, list())
        self._selection = FlowSelection()

        self._history = FlowHistory(max_history=self.options.max_history)
        self._history.save_history("Deserialized graph", self)

    @property
    def key(self):
        return GraphKey(self.uuid)

    @key.setter
    def key(self, value: GraphKey) -> None:
        self.uuid = str(value)

    @property
    def selection(self):
        return self._selection

    @property
    def selected_wire_only(self) -> Optional[FlowWire]:
        return self._selection.selected_wire_only

    @property
    def history(self):
        return self._history

    def restore(self, other: "FlowGraph") -> None:
        if self.uuid != other.uuid:
            raise ValueError("The uuid of the graph to be restored does not match")

        self.name = other.name
        self.docs = other.docs
        self.icon = other.icon
        self.nodes = other.nodes
        self.wires = other.wires
        self.variables = other.variables
        self.control = other.control
        self.options = other.options
        self.tags = other.tags
        self._selection = other._selection
        self._history = other._history

    def clear_history(self) -> None:
        logger.info("Clear history")
        self.history.clear_history()

    def save_history(
        self,
        title: str,
        details: Optional[str] = None,
        *,
        no_logging=False,
    ) -> None:
        if not no_logging:
            logger.info(title)
            if details:
                logger.debug(details)

        self.history.save_history(
            title=title,
            value=self,
            details=details,
            max_history=self.options.max_history,
        )

    def load_history(self, index: int, *, no_logging=False) -> None:
        if not no_logging:
            logger.info(f"Load history: {index}")
        self.restore(self.history.load_history(index))

    def undo_history(self, *, no_logging=False) -> None:
        if not self.history.undoable:
            raise ValueError("History is not undoable")
        if not no_logging:
            logger.info("Undo history")
        self.load_history(self.history.cursor_index - 1, no_logging=True)

    def redo_history(self, *, no_logging=False) -> None:
        if not self.history.redoable:
            raise ValueError("History is not redoable")
        if not no_logging:
            logger.info("Redo history")
        self.load_history(self.history.cursor_index + 1, no_logging=True)

    def paste_selection(
        self,
        items: FlowSelection,
        point: Point,
        *,
        selected: Optional[bool] = None,
    ) -> None:
        nodes, wires, variables = items.copy_validated_items(point)

        if selected is not None:
            for node in nodes:
                for pin in node.pins:
                    pin.selected = False
                node.selected = selected
            for wire in wires:
                wire.selected = selected
            for variable in variables:
                variable.selected = selected

        for node in nodes:
            self.nodes.insert(0, node)
        for wire in wires:
            self.wires.insert(0, wire)
        for variable in variables:
            self.variables.insert(0, variable)

        self.update_selected_items()
        self.update_wires_polyline(force=True)

    def update_selected_item(self, item: FlowSelectableAny) -> None:
        self._selection.apply(item)

    def update_selected_items(self) -> None:
        for node in self.nodes:
            for pin in node.pins:
                self._selection.apply(pin)
            self._selection.apply(node)
        for wire in self.wires:
            self._selection.apply(wire)
        for variable in self.variables:
            self._selection.apply(variable)

    def update_selected_nodes(self) -> None:
        for node in self.nodes:
            self._selection.apply(node)

    def update_selected_wires(self) -> None:
        for wire in self.wires:
            self._selection.apply(wire)

    def update_selected_variables(self) -> None:
        for variable in self.variables:
            self._selection.apply(variable)

    def select_item(self, item: FlowSelectableAny, *, selected=True) -> None:
        item.selected = selected
        if selected:
            self._selection.add(item)
        else:
            self._selection.remove_noraise(item)

    def select_all_nodes(self) -> None:
        for node in self.nodes:
            self.select_item(node)

    def select_all_wires(self) -> None:
        for wire in self.wires:
            self.select_item(wire)

    def select_all_pins(self) -> None:
        for node in self.nodes:
            for pin in node.pins:
                self.select_item(pin)

    def select_all_items(self) -> None:
        self.select_all_nodes()
        self.select_all_wires()

    def unselect_item(self, item: FlowSelectableAny) -> None:
        self.select_item(item, selected=False)

    def flip_select_item(self, item: FlowSelectableAny) -> None:
        self.select_item(item, selected=not item.selected)

    def clear_state(self) -> None:
        # Do not change the `node.selected` property.
        for node in self.nodes:
            node.hovering = False
            for pin in node.pins:
                pin.hovering = False
                pin.connectable = False

        for wire in self.wires:
            wire.hovering = False
            wire.start_anchor.hovering = False
            wire.end_anchor.hovering = False

        for variable in self.variables:
            variable.hovering = False

    def find_node(self, node_uuid: str) -> Optional[FlowNode]:
        return self.nodes.get(node_uuid)

    def create_node_pin(
        self,
        node: Union[FlowNode, str],
        pin: Union[FlowPin, str],
    ) -> FlowNodePin:
        if isinstance(node, str):
            node_ = self.find_node(node)
            if node_ is None:
                raise IndexError(f"Not found '{node}' node in the '{self.name}' graph")
            node = node_
        elif isinstance(node, FlowNode):
            if self.nodes.index(node) < 0:
                raise IndexError(
                    f"The '{node.name}' node does not exist in the '{self.name}' graph"
                )
        else:
            raise TypeError(f"Unsupported node type: {type(node).__name__}")

        assert isinstance(node, FlowNode)

        if isinstance(pin, str):
            pin_ = node.find_pin(pin)
            if pin_ is None:
                raise IndexError(f"Not found '{pin}' pin in the '{node.name}' node")
            pin = pin_
        elif isinstance(pin, FlowPin):
            if node.pins.index(pin) < 0:
                raise IndexError(
                    f"The '{pin.name}' pin does not exist in the '{node.name}' node"
                )
        else:
            raise TypeError(f"Unsupported pin type: {type(pin).__name__}")

        assert isinstance(pin, FlowPin)

        return FlowNodePin(node, pin)

    def find_begin_nodes(self) -> List[FlowNode]:
        return list(filter(lambda node: node.is_begin, self.nodes))

    def find_begin_node(self, node_uuid: str) -> Optional[FlowNode]:
        for node in self.find_begin_nodes():
            if node.uuid == node_uuid:
                return node
        return None

    def find_hovering_node_with_mouse(self, mouse: Point) -> Optional[FlowNode]:
        mx, my = mouse
        for node in self.nodes:
            x1, y1, x2, y2 = node.node_roi
            left = min(x1, x2)
            right = max(x1, x2)
            top = min(y1, y2)
            bottom = max(y1, y2)
            if left <= mx <= right and top <= my <= bottom:
                return node
        return None

    def find_hovering_node(self) -> Optional[FlowNode]:
        for node in self.nodes:
            if node.hovering:
                return node
        return None

    def find_hovering_pin(self) -> Optional[FlowNodePin]:
        node = self.find_hovering_node()
        if node is None:
            return None

        if not node.hovering:
            raise ValueError("Only hovering nodes are allowed")

        pin = node.find_hovering_pin()
        if pin is None:
            return None

        return FlowNodePin(node, pin)

    def find_hovering_wire_with_mouse(self, mouse: Point) -> Optional[FlowWire]:
        mp = shapely.Point(mouse)
        for wire in self.wires:
            distance = shapely.LineString(wire.polyline).distance(mp)
            if distance <= self.options.line_hovering_tolerance:
                return wire
        return None

    def find_hovering_wire(self) -> Optional[FlowWire]:
        for wire in self.wires:
            if wire.hovering:
                return wire
        return None

    def find_variable(self, key: str) -> Optional[FlowVariable]:
        return self.variables.get(key)

    def find_hovering_variable(self) -> Optional[FlowVariable]:
        for variable in self.variables:
            if variable.hovering:
                return variable
        return None

    def find_hovering_anchor_with_mouse(
        self,
        wire: FlowWire,
        mouse: Point,
    ) -> Optional[FlowAnchor]:
        mx, my = mouse

        start, end = wire.get_bezier_cubic_anchors()
        sx, sy = start
        sdx = mx - sx
        sdy = my - sy
        start_distance = sqrt(sdx**2 + sdy**2)
        if start_distance <= self.options.anchor_hovering_tolerance:
            return wire.start_anchor

        ex, ey = end
        edx = mx - ex
        edy = my - ey
        end_distance = sqrt(edx**2 + edy**2)
        if end_distance <= self.options.anchor_hovering_tolerance:
            return wire.end_anchor
        return None

    def find_hovering_anchor(self) -> Optional[FlowAnchor]:
        if selected_wire := self.selected_wire_only:
            if selected_wire.start_anchor.hovering:
                return selected_wire.start_anchor
            if selected_wire.end_anchor.hovering:
                return selected_wire.end_anchor
        return None

    def find_hovering_item(self) -> Optional[FlowSelectableAny]:
        if node := self.find_hovering_node():
            assert node.hovering

            if pin := node.find_hovering_pin():
                assert pin.hovering
                return pin

            return node

        if wire := self.find_hovering_wire():
            assert wire.hovering
            return wire

        if variable := self.find_hovering_variable():
            assert variable.hovering
            return variable

        return None

    def pop_wires(self, uuids: Union[Set[str], Iterable[str]]) -> List[FlowWire]:
        if not isinstance(uuids, set):
            uuids = set(uuids)
        remain_wires = list()
        pop_wires = list()
        for wire in self.wires:
            if wire.uuid in uuids:
                pop_wires.append(wire)
            else:
                remain_wires.append(wire)
        self.wires.clear()
        self.wires.extend(remain_wires)
        return pop_wires

    def find_selected_wires(self) -> List[FlowWire]:
        result = list()
        for wire in self.wires:
            if wire.selected:
                result.append(wire)
        return result

    def find_selected_pins(self) -> List[FlowPin]:
        result = list()
        for node in self.nodes:
            result.extend(node.find_selected_pins())
        return result

    def find_selected_nodes(self) -> List[FlowNode]:
        result = list()
        for node in self.nodes:
            if node.selected:
                result.append(node)
        return result

    def find_selected_variables(self) -> List[FlowVariable]:
        result = list()
        for variable in self.variables:
            if variable.selected:
                result.append(variable)
        return result

    def unselect_all_items(self) -> None:
        for node in self.nodes:
            node.selected = False

            for pin in node.pins:
                pin.selected = False

        for wire in self.wires:
            wire.selected = False
            wire.start_anchor.selected = False
            wire.end_anchor.selected = False

        for variable in self.variables:
            variable.selected = False

        self._selection.clear()

    def flip_selected_on_hovering_item(self) -> Optional[FlowSelectableAny]:
        if node := self.find_hovering_node():
            assert node.hovering

            if pin := node.find_hovering_pin():
                assert pin.hovering
                pin.selected = not pin.selected
                self._selection.apply(pin)
                return pin
            else:
                node.selected = not node.selected
                self._selection.apply(node)
                return node

        if wire := self.find_hovering_wire():
            assert wire.hovering
            wire.selected = not wire.selected
            self._selection.apply(wire)
            return wire

        if variable := self.find_hovering_variable():
            assert variable.hovering
            variable.selected = not variable.selected
            self._selection.apply(variable)
            return variable

        return None

    def move_node(self, node: FlowNode, pos: Point) -> None:
        node.node_pos = pos
        for pin in node.pins:
            for wire_uuid in pin.wires:
                if wire := self.wires.get(wire_uuid):
                    self.update_wire_polyline(wire, force=True)

    def move_on_selected_nodes(self, delta: Size) -> None:
        dx, dy = delta
        if dx == 0 and dy == 0:
            return

        for node in self.nodes:
            if not node.selected:
                continue

            x, y = node.node_pos
            next_pos = x + dx, y + dy
            self.move_node(node, next_pos)

    def move_on_selected_anchor(self, delta: Size) -> None:
        dx, dy = delta
        if dx == 0 and dy == 0:
            return

        selected_wire = self.selected_wire_only
        if selected_wire is None:
            return

        if selected_wire.start_anchor.selected:
            selected_wire.start_anchor.x += dx
            selected_wire.start_anchor.y += dy

        if selected_wire.end_anchor.selected:
            selected_wire.end_anchor.x += dx
            selected_wire.end_anchor.y += dy

        self.update_wire_polyline(selected_wire, force=True)

    def update_wires_io(self, *, force=False) -> None:
        for wire in self.wires:
            self.update_wire_io(wire, force=force)

    def update_wire_io(self, wire: FlowWire, *, force=False) -> None:
        self.update_wire_output(wire, force=force)
        self.update_wire_input(wire, force=force)

    def update_wire_output(self, wire: FlowWire, *, force=False) -> None:
        if not force and wire.output is not None:
            return

        for node in self.nodes:
            if pin := node.find_output_pin(wire.uuid):
                wire.output = FlowNodePin(node, pin)
                return

        raise IndexError("Could not find the output pin of the wire")

    def update_wire_input(self, wire: FlowWire, *, force=False) -> None:
        if not force and wire.input is not None:
            return

        for node in self.nodes:
            if pin := node.find_input_pin(wire.uuid):
                wire.input = FlowNodePin(node, pin)
                return

        raise IndexError("Could not find the input pin of the wire")

    def update_wires_polyline(self, *, force=False) -> None:
        for wire in self.wires:
            self.update_wire_polyline(wire, force=force)

    def update_wire_polyline(self, wire: FlowWire, *, force=False) -> None:
        if not force and wire.polyline:
            return

        if wire.output is None:
            self.update_wire_output(wire)

        if wire.input is None:
            self.update_wire_input(wire)

        assert wire.output is not None
        assert wire.input is not None
        wire.update_polyline(self.options.bezier_curve_tessellation_tolerance)

    def connect_pins(
        self,
        out_conn: FlowNodePin,
        in_conn: FlowNodePin,
        *,
        no_reorder=False,
    ) -> FlowWire:
        if not no_reorder:
            connection_pair = FlowConnection.reorder_connectable_pins(out_conn, in_conn)
            out_conn, in_conn = connection_pair

        wire = FlowWire.from_connect_pair(
            out_conn,
            in_conn,
            self.options.bezier_curve_tessellation_tolerance,
            name=f"{out_conn.pin.name}-{out_conn.pin.name}",
            docs=f"{str(out_conn)}-{str(out_conn)}",
        )
        self.wires.append(wire)
        out_conn.pin.wires.append(wire.uuid)
        in_conn.pin.wires.append(wire.uuid)

        return wire

    def update_hovering_state(self, mouse: Point) -> None:
        if hovering_node := self.find_hovering_node_with_mouse(mouse):
            hovering_node.hovering = True
            if hovering_pin := hovering_node.find_hovering_pin_with_mouse(mouse):
                hovering_pin.hovering = True
            return

        hovering_wire = self.find_hovering_wire_with_mouse(mouse)
        if hovering_wire is not None:
            hovering_wire.hovering = True

        if selected_wire := self.selected_wire_only:
            if anchor := self.find_hovering_anchor_with_mouse(selected_wire, mouse):
                anchor.hovering = True

    def remove_variable(self, variable: FlowVariable) -> None:
        self.variables.remove(variable)
        self._selection.remove_noraise(variable)

    def remove_selected_variable(self) -> None:
        for variable in self.find_selected_variables():
            self.remove_variable(variable)

    def remove_wire(self, wire: FlowWire) -> None:
        if wire.input:
            wire.input.pin.wires.remove(wire.uuid)
        if wire.output:
            wire.output.pin.wires.remove(wire.uuid)
        self.wires.remove(wire)
        self._selection.remove_noraise(wire)

    def remove_selected_wires(self) -> None:
        for wire in self.find_selected_wires():
            self.remove_wire(wire)

    def remove_node(self, node: FlowNode):
        for pin in node.pins:
            for wire_uuid in pin.wires:
                if wire := self.wires.get(wire_uuid):
                    self.remove_wire(wire)
            self._selection.remove_noraise(pin)
        self.nodes.remove(node)
        self._selection.remove_noraise(node)

    def remove_selected_nodes(self) -> None:
        for node in self.find_selected_nodes():
            self.remove_node(node)

    def remove_selected_items(self) -> None:
        self.remove_selected_nodes()
        self.remove_selected_wires()
        self.remove_selected_variable()

    def items_to_front(self, items: Iterable[FlowSelectableAny]) -> None:
        for item in items:
            self.item_to_front(item)

    def item_to_front(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_to_front(item)
        elif isinstance(item, FlowWire):
            self.wire_to_front(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_to_front(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if 0 <= index - 1:
            assert node == self.nodes.pop(index)
            self.nodes.insert(index - 1, node)

    def wire_to_front(self, wire: FlowWire) -> None:
        index = self.wires.index(wire)
        if 0 <= index - 1:
            assert wire == self.wires.pop(index)
            self.wires.insert(index - 1, wire)

    def items_to_back(self, items: Iterable[FlowSelectableAny]) -> None:
        for item in items:
            self.item_to_back(item)

    def item_to_back(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_to_back(item)
        elif isinstance(item, FlowWire):
            self.wire_to_back(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_to_back(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if index + 1 < len(self.nodes):
            assert node == self.nodes.pop(index)
            self.nodes.insert(index + 1, node)

    def wire_to_back(self, wire: FlowWire) -> None:
        index = self.wires.index(wire)
        if index + 1 < len(self.wires):
            assert wire == self.wires.pop(index)
            self.wires.insert(index + 1, wire)

    def item_bring_forward(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_bring_forward(item)
        elif isinstance(item, FlowWire):
            self.wire_bring_forward(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_bring_forward(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if 0 != index:
            assert node == self.nodes.pop(index)
            self.nodes.insert(0, node)

    def wire_bring_forward(self, wire: FlowWire) -> None:
        index = self.wires.index(wire)
        if 0 != index:
            assert wire == self.wires.pop(index)
            self.wires.insert(0, wire)

    def item_send_backward(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_send_backward(item)
        elif isinstance(item, FlowWire):
            self.wire_send_backward(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_send_backward(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if index < len(self.wires) - 1:
            assert node == self.nodes.pop(index)
            self.nodes.append(node)

    def wire_send_backward(self, wire: FlowWire) -> None:
        index = self.wires.index(wire)
        if index < len(self.wires) - 1:
            assert wire == self.wires.pop(index)
            self.wires.append(wire)

    def nodes_align_left(self, nodes: Iterable[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            px, py = pivot.node_pos
            next_pox = px, ny
            self.move_node(node, next_pox)

    def nodes_align_center(self, nodes: Iterable[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = px + (pw / 2) - (nw / 2), ny
            self.move_node(node, next_pos)

    def nodes_align_right(self, nodes: Iterable[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = px + pw - nw, ny
            self.move_node(node, next_pos)

    def nodes_align_top(self, nodes: Iterable[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            px, py = pivot.node_pos
            next_pox = nx, py
            self.move_node(node, next_pox)

    def nodes_align_middle(self, nodes: Iterable[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = nx, py + (ph / 2) - (nh / 2)
            self.move_node(node, next_pos)

    def nodes_align_bottom(self, nodes: Iterable[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = nx, py + ph - nh
            self.move_node(node, next_pos)

    def nodes_distribute_horizontal(self, nodes: Iterable[FlowNode]) -> None:
        nx1s = [n.x1 for n in nodes]
        nx2s = [n.x2 for n in nodes]
        nws = [n.width for n in nodes]
        width = reduce(lambda w1, w2: w1 + w2, nws)
        left = min(nx1s)
        right = max(nx2s)
        space = (right - left - width) / (len(nws) - 1)
        nodes = sorted(nodes, key=lambda n: n.x1)
        cursor = left

        for node in nodes:
            y1 = node.y1
            next_pos = cursor, y1
            self.move_node(node, next_pos)
            cursor += node.width + space

    def nodes_distribute_vertical(self, nodes: Iterable[FlowNode]) -> None:
        ny1s = [n.y1 for n in nodes]
        ny2s = [n.y2 for n in nodes]
        nhs = [n.height for n in nodes]
        height = reduce(lambda h1, h2: h1 + h2, nhs)
        top = min(ny1s)
        bottom = max(ny2s)
        space = (bottom - top - height) / (len(nhs) - 1)
        nodes = sorted(nodes, key=lambda n: n.y1)
        cursor = top

        for node in nodes:
            x1 = node.x1
            next_pos = x1, cursor
            self.move_node(node, next_pos)
            cursor += node.height + space

    def add_variable(self, name: str, dtype: Dtype) -> FlowVariable:
        result = FlowVariable(
            key=VariableKey(name),
            dtype=dtype,
            docs=None,
            value=dtype(),
            initial=dtype(),
        )  # type: ignore[var-annotated]
        self.variables.append(result)
        return result

    def retrieve_data_node_execution_order(self, node: FlowNode) -> List[FlowNodePin]:
        result = list()
        for data_input in node.data_inputs:
            for wire_uuid in data_input.wires:
                wire = self.wires.get(wire_uuid)
                assert wire is not None

                prev_np = wire.output
                if prev_np is None:
                    raise ValueError("Output node-pin is not cached")

                prev_node = prev_np.node
                if not prev_node.is_data_only:
                    continue

                result.extend(self.retrieve_data_node_execution_order(prev_node))
                result.append(prev_np)
        return result
