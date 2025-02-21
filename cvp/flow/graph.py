# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from enum import StrEnum, auto, unique
from functools import reduce
from math import sqrt
from typing import Any, Dict, List, Optional, Sequence, Set, Union
from uuid import uuid4

import shapely
from type_serialize import Serializable, deserialize, serialize

from cvp.containers.mapping_deque import MappingDeque
from cvp.dtypes.dtype import Dtype
from cvp.flow.anchor import FlowAnchor
from cvp.flow.arc import FlowArc
from cvp.flow.connection import FlowConnection
from cvp.flow.control import FlowControl
from cvp.flow.node import FlowNode
from cvp.flow.node_pin import FlowNodePin
from cvp.flow.pin import FlowPin
from cvp.flow.selection import FlowSelectableAny, FlowSelection
from cvp.flow.variable import FlowVariable
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.override import override
from cvp.types.shapes import Point, Size


@unique
class FlowGraphKeys(StrEnum):
    uuid = auto()
    name_ = "name"
    docs = auto()
    icon = auto()
    lock = auto()
    color = auto()
    nodes = auto()
    arcs = auto()
    variables = auto()
    control = auto()
    tags = auto()


class FlowGraph(Serializable):
    Keys = FlowGraphKeys

    def __init__(
        self,
        uuid: Optional[str] = None,
        name: Optional[str] = None,
        docs: Optional[str] = None,
        icon: Optional[str] = None,
        lock=False,
        color: RGBA = WHITE_RGBA,
        nodes: Optional[Sequence[FlowNode]] = None,
        arcs: Optional[Sequence[FlowArc]] = None,
        variables: Optional[Sequence[FlowVariable]] = None,
        control: Optional[FlowControl] = None,
        tags: Optional[Sequence[str]] = None,
        *,
        selection: Optional[FlowSelection] = None,
    ):
        self.uuid = uuid if uuid else str(uuid4())
        self.name = name if name else str()
        self.docs = docs if docs else str()
        self.icon = icon if icon else str()
        self.lock = lock
        self.color = color

        self.nodes = MappingDeque[str, FlowNode](nodes, keyable=self._node_keyable)
        self.arcs = MappingDeque[str, FlowArc](arcs, keyable=self._arc_keyable)
        self.variables = MappingDeque[str, FlowVariable](
            variables,
            keyable=self._variable_keyable,
        )

        self.control = control if control else FlowControl()
        self.tags = list(tags if tags else ())
        self._selection = selection if selection else FlowSelection()

    @staticmethod
    def _node_keyable(node: FlowNode) -> str:
        return node.uuid

    @staticmethod
    def _arc_keyable(arc: FlowArc) -> str:
        return arc.uuid

    @staticmethod
    def _variable_keyable(variable: FlowVariable) -> str:
        return variable.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.uuid == other.uuid
            and self.name == other.name
            and self.docs == other.docs
            and self.icon == other.icon
            and self.lock == other.lock
            and self.color == other.color
            and self.nodes == other.nodes
            and self.arcs == other.arcs
            and self.variables == other.variables
            and self.control == other.control
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
        result.color = copy(self.color)
        result.nodes = copy(self.nodes)
        result.arcs = copy(self.arcs)
        result.variables = copy(self.variables)
        result.control = copy(self.control)
        result.tags = copy(self.tags)
        result._selection = copy(self._selection)
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
        result.color = deepcopy(self.color, memo)
        result.nodes = deepcopy(self.nodes, memo)
        result.arcs = deepcopy(self.arcs, memo)
        result.variables = deepcopy(self.variables, memo)
        result.control = deepcopy(self.control, memo)
        result.tags = deepcopy(self.tags, memo)
        result._selection = deepcopy(self._selection, memo)
        memo[id(self)] = result
        return result

    @override
    def __serialize__(self) -> Any:
        result = {
            self.Keys.uuid: self.uuid,
            self.Keys.name_: self.name,
            self.Keys.docs: self.docs,
            self.Keys.icon: self.icon,
            self.Keys.lock: self.lock,
            self.Keys.color: self.color,
            self.Keys.nodes: serialize(self.nodes.as_list()),
            self.Keys.arcs: serialize(self.arcs.as_list()),
            self.Keys.variables: serialize(self.variables.as_list()),
            self.Keys.control: serialize(self.control),
            self.Keys.tags: self.tags,
        }
        return {str(key): val for key, val in result.items()}

    @override
    def __deserialize__(self, data: Any) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Unexpected data type: {type(data).__name__}")

        self.uuid = data.get(self.Keys.uuid, str())
        self.name = data.get(self.Keys.name_, str())
        self.docs = data.get(self.Keys.docs, str())
        self.icon = data.get(self.Keys.icon, str())
        self.lock = data.get(self.Keys.lock, False)
        self.color = data.get(self.Keys.color, WHITE_RGBA)

        self.nodes = MappingDeque(keyable=self._node_keyable)
        self.arcs = MappingDeque(keyable=self._arc_keyable)
        self.variables = MappingDeque(keyable=self._variable_keyable)

        if nodes := data.get(self.Keys.nodes):
            for node in nodes:
                self.nodes.append(deserialize(node, FlowNode))
        if arcs := data.get(self.Keys.arcs):
            for arc in arcs:
                self.arcs.append(deserialize(arc, FlowArc))
        if variables := data.get(self.Keys.variables):
            for variable in variables:
                self.variables.append(deserialize(variable, FlowVariable))

        if control := data.get(self.Keys.control):
            self.control = deserialize(control, FlowControl)
        else:
            self.control = FlowControl()

        self.tags = data.get(self.Keys.tags, list())

    @property
    def selection(self):
        return self._selection

    @property
    def selected_arc_only(self) -> Optional[FlowArc]:
        return self._selection.selected_arc_only

    def restore(self, other: "FlowGraph") -> None:
        if self.uuid != other.uuid:
            raise ValueError("The uuid of the graph to be restored does not match")

        self.name = other.name
        self.docs = other.docs
        self.icon = other.icon
        self.nodes = other.nodes
        self.arcs = other.arcs
        self.variables = other.variables
        self.control = other.control
        self.tags = other.tags
        self._selection = other._selection

    def paste_selection(
        self,
        items: FlowSelection,
        point: Point,
        *,
        selected: Optional[bool] = None,
    ) -> None:
        nodes, arcs, variables = items.copy_validated_items(point)

        if selected is not None:
            for node in nodes:
                for pin in node.pins:
                    pin.selected = False
                node.selected = selected
            for arc in arcs:
                arc.selected = selected
            for variable in variables:
                variable.selected = selected

        for node in nodes:
            self.nodes.insert(0, node)
        for arc in arcs:
            self.arcs.insert(0, arc)
        for variable in variables:
            self.variables.insert(0, variable)

        self.update_selected_items()
        self.update_arcs_polyline(force=True)

    def update_selected_item(self, item: FlowSelectableAny) -> None:
        self._selection.apply(item)

    def update_selected_items(self) -> None:
        for node in self.nodes:
            for pin in node.pins:
                self._selection.apply(pin)
            self._selection.apply(node)
        for arc in self.arcs:
            self._selection.apply(arc)
        for variable in self.variables:
            self._selection.apply(variable)

    def update_selected_nodes(self) -> None:
        for node in self.nodes:
            self._selection.apply(node)

    def update_selected_arcs(self) -> None:
        for arc in self.arcs:
            self._selection.apply(arc)

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

    def select_all_arcs(self) -> None:
        for arc in self.arcs:
            self.select_item(arc)

    def select_all_pins(self) -> None:
        for node in self.nodes:
            for pin in node.pins:
                self.select_item(pin)

    def select_all_items(self) -> None:
        self.select_all_nodes()
        self.select_all_arcs()

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

        for arc in self.arcs:
            arc.hovering = False
            arc.start_anchor.hovering = False
            arc.end_anchor.hovering = False

        for variable in self.variables:
            variable.hovering = False

    def find_node(self, node_uuid: str) -> Optional[FlowNode]:
        for node in self.nodes:
            if node.uuid == node_uuid:
                return node
        return None

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

    def find_hovering_arc_with_mouse(self, mouse: Point) -> Optional[FlowArc]:
        mp = shapely.Point(mouse)
        for arc in self.arcs:
            distance = shapely.LineString(arc.polyline).distance(mp)
            if distance <= self.control.arc_hovering_tolerance:
                return arc
        return None

    def find_hovering_arc(self) -> Optional[FlowArc]:
        for arc in self.arcs:
            if arc.hovering:
                return arc
        return None

    def find_variable(self, key: str) -> Optional[FlowVariable]:
        for variable in self.variables:
            if variable.name == key:
                return variable
        return None

    def find_hovering_variable(self) -> Optional[FlowVariable]:
        for variable in self.variables:
            if variable.hovering:
                return variable
        return None

    def find_hovering_anchor_with_mouse(
        self,
        arc: FlowArc,
        mouse: Point,
    ) -> Optional[FlowAnchor]:
        mx, my = mouse

        start, end = arc.get_bezier_cubic_anchors()
        sx, sy = start
        sdx = mx - sx
        sdy = my - sy
        start_distance = sqrt(sdx**2 + sdy**2)
        if start_distance <= self.control.anchor_hovering_tolerance:
            return arc.start_anchor

        ex, ey = end
        edx = mx - ex
        edy = my - ey
        end_distance = sqrt(edx**2 + edy**2)
        if end_distance <= self.control.anchor_hovering_tolerance:
            return arc.end_anchor
        return None

    def find_hovering_anchor(self) -> Optional[FlowAnchor]:
        if selected_arc := self.selected_arc_only:
            if selected_arc.start_anchor.hovering:
                return selected_arc.start_anchor
            if selected_arc.end_anchor.hovering:
                return selected_arc.end_anchor
        return None

    def find_hovering_item(self) -> Optional[FlowSelectableAny]:
        if node := self.find_hovering_node():
            assert node.hovering

            if pin := node.find_hovering_pin():
                assert pin.hovering
                return pin

            return node

        if arc := self.find_hovering_arc():
            assert arc.hovering
            return arc

        if variable := self.find_hovering_variable():
            assert variable.hovering
            return variable

        return None

    def find_arc(self, arc_uuid: str) -> Optional[FlowArc]:
        for arc in self.arcs:
            if arc.uuid == arc_uuid:
                return arc
        return None

    def pop_arcs(self, uuids: Union[Set[str], Sequence[str]]) -> List[FlowArc]:
        if not isinstance(uuids, set):
            uuids = set(uuids)
        remain_arcs = list()
        pop_arcs = list()
        for arc in self.arcs:
            if arc.uuid in uuids:
                pop_arcs.append(arc)
            else:
                remain_arcs.append(arc)
        self.arcs.clear()
        self.arcs.extend(remain_arcs)
        return pop_arcs

    def find_selected_arcs(self) -> List[FlowArc]:
        result = list()
        for arc in self.arcs:
            if arc.selected:
                result.append(arc)
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

        for arc in self.arcs:
            arc.selected = False
            arc.start_anchor.selected = False
            arc.end_anchor.selected = False

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

        if arc := self.find_hovering_arc():
            assert arc.hovering
            arc.selected = not arc.selected
            self._selection.apply(arc)
            return arc

        if variable := self.find_hovering_variable():
            assert variable.hovering
            variable.selected = not variable.selected
            self._selection.apply(variable)
            return variable

        return None

    def move_node(self, node: FlowNode, pos: Point) -> None:
        node.node_pos = pos
        for pin in node.pins:
            for arc_uuid in pin.arcs:
                if arc := self.find_arc(arc_uuid):
                    self.update_arc_polyline(arc, force=True)

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

        selected_arc = self.selected_arc_only
        if selected_arc is None:
            return

        if selected_arc.start_anchor.selected:
            selected_arc.start_anchor.x += dx
            selected_arc.start_anchor.y += dy

        if selected_arc.end_anchor.selected:
            selected_arc.end_anchor.x += dx
            selected_arc.end_anchor.y += dy

        self.update_arc_polyline(selected_arc, force=True)

    def update_arcs_io(self, *, force=False) -> None:
        for arc in self.arcs:
            self.update_arc_io(arc, force=force)

    def update_arc_io(self, arc: FlowArc, *, force=False) -> None:
        self.update_arc_output(arc, force=force)
        self.update_arc_input(arc, force=force)

    def update_arc_output(self, arc: FlowArc, *, force=False) -> None:
        if not force and arc.output is not None:
            return

        for node in self.nodes:
            if pin := node.find_output_pin(arc.uuid):
                arc.output = FlowNodePin(node, pin)
                return

        raise IndexError("Could not find the output pin of the arc")

    def update_arc_input(self, arc: FlowArc, *, force=False) -> None:
        if not force and arc.input is not None:
            return

        for node in self.nodes:
            if pin := node.find_input_pin(arc.uuid):
                arc.input = FlowNodePin(node, pin)
                return

        raise IndexError("Could not find the input pin of the arc")

    def update_arcs_polyline(self, *, force=False) -> None:
        for arc in self.arcs:
            self.update_arc_polyline(arc, force=force)

    def update_arc_polyline(self, arc: FlowArc, *, force=False) -> None:
        if not force and arc.polyline:
            return

        if arc.output is None:
            self.update_arc_output(arc)

        if arc.input is None:
            self.update_arc_input(arc)

        assert arc.output is not None
        assert arc.input is not None
        arc.update_polyline(self.control.bezier_curve_tessellation_tolerance)

    def connect_pins(
        self,
        out_conn: FlowNodePin,
        in_conn: FlowNodePin,
        *,
        no_reorder=False,
    ) -> FlowArc:
        if not no_reorder:
            connection_pair = FlowConnection.reorder_connectable_pins(out_conn, in_conn)
            out_conn, in_conn = connection_pair

        arc = FlowArc.from_connect_pair(
            out_conn,
            in_conn,
            self.control.bezier_curve_tessellation_tolerance,
        )
        self.arcs.append(arc)
        out_conn.pin.arcs.append(arc.uuid)
        in_conn.pin.arcs.append(arc.uuid)

        return arc

    def update_hovering_state(self, mouse: Point) -> None:
        if hovering_node := self.find_hovering_node_with_mouse(mouse):
            hovering_node.hovering = True
            if hovering_pin := hovering_node.find_hovering_pin_with_mouse(mouse):
                hovering_pin.hovering = True
            return

        hovering_arc = self.find_hovering_arc_with_mouse(mouse)
        if hovering_arc is not None:
            hovering_arc.hovering = True

        if selected_arc_only := self.selected_arc_only:
            if anchor := self.find_hovering_anchor_with_mouse(selected_arc_only, mouse):
                anchor.hovering = True

    def remove_variable(self, variable: FlowVariable) -> None:
        self.variables.remove(variable)
        self._selection.remove_noraise(variable)

    def remove_selected_variable(self) -> None:
        for variable in self.find_selected_variables():
            self.remove_variable(variable)

    def remove_arc(self, arc: FlowArc) -> None:
        if arc.input:
            arc.input.pin.arcs.remove(arc.uuid)
        if arc.output:
            arc.output.pin.arcs.remove(arc.uuid)
        self.arcs.remove(arc)
        self._selection.remove_noraise(arc)

    def remove_selected_arcs(self) -> None:
        for arc in self.find_selected_arcs():
            self.remove_arc(arc)

    def remove_node(self, node: FlowNode):
        for pin in node.pins:
            for arc_uuid in pin.arcs:
                if arc := self.find_arc(arc_uuid):
                    self.remove_arc(arc)
            self._selection.remove_noraise(pin)
        self.nodes.remove(node)
        self._selection.remove_noraise(node)

    def remove_selected_nodes(self) -> None:
        for node in self.find_selected_nodes():
            self.remove_node(node)

    def remove_selected_items(self) -> None:
        self.remove_selected_nodes()
        self.remove_selected_arcs()
        self.remove_selected_variable()

    def items_to_front(self, items: Sequence[FlowSelectableAny]) -> None:
        for item in items:
            self.item_to_front(item)

    def item_to_front(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_to_front(item)
        elif isinstance(item, FlowArc):
            self.arc_to_front(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_to_front(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if 0 <= index - 1:
            assert node == self.nodes.pop(index)
            self.nodes.insert(index - 1, node)

    def arc_to_front(self, arc: FlowArc) -> None:
        index = self.arcs.index(arc)
        if 0 <= index - 1:
            assert arc == self.arcs.pop(index)
            self.arcs.insert(index - 1, arc)

    def items_to_back(self, items: Sequence[FlowSelectableAny]) -> None:
        for item in items:
            self.item_to_back(item)

    def item_to_back(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_to_back(item)
        elif isinstance(item, FlowArc):
            self.arc_to_back(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_to_back(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if index + 1 < len(self.nodes):
            assert node == self.nodes.pop(index)
            self.nodes.insert(index + 1, node)

    def arc_to_back(self, arc: FlowArc) -> None:
        index = self.arcs.index(arc)
        if index + 1 < len(self.arcs):
            assert arc == self.arcs.pop(index)
            self.arcs.insert(index + 1, arc)

    def item_bring_forward(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_bring_forward(item)
        elif isinstance(item, FlowArc):
            self.arc_bring_forward(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_bring_forward(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if 0 != index:
            assert node == self.nodes.pop(index)
            self.nodes.insert(0, node)

    def arc_bring_forward(self, arc: FlowArc) -> None:
        index = self.arcs.index(arc)
        if 0 != index:
            assert arc == self.arcs.pop(index)
            self.arcs.insert(0, arc)

    def item_send_backward(self, item: FlowSelectableAny) -> None:
        if isinstance(item, FlowNode):
            self.node_send_backward(item)
        elif isinstance(item, FlowArc):
            self.arc_send_backward(item)
        elif isinstance(item, (FlowPin, FlowVariable)):
            pass
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_send_backward(self, node: FlowNode) -> None:
        index = self.nodes.index(node)
        if index < len(self.arcs) - 1:
            assert node == self.nodes.pop(index)
            self.nodes.append(node)

    def arc_send_backward(self, arc: FlowArc) -> None:
        index = self.arcs.index(arc)
        if index < len(self.arcs) - 1:
            assert arc == self.arcs.pop(index)
            self.arcs.append(arc)

    def nodes_align_left(self, nodes: Sequence[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            px, py = pivot.node_pos
            next_pox = px, ny
            self.move_node(node, next_pox)

    def nodes_align_center(self, nodes: Sequence[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = px + (pw / 2) - (nw / 2), ny
            self.move_node(node, next_pos)

    def nodes_align_right(self, nodes: Sequence[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = px + pw - nw, ny
            self.move_node(node, next_pos)

    def nodes_align_top(self, nodes: Sequence[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            px, py = pivot.node_pos
            next_pox = nx, py
            self.move_node(node, next_pox)

    def nodes_align_middle(self, nodes: Sequence[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = nx, py + (ph / 2) - (nh / 2)
            self.move_node(node, next_pos)

    def nodes_align_bottom(self, nodes: Sequence[FlowNode], pivot: FlowNode) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = nx, py + ph - nh
            self.move_node(node, next_pos)

    def nodes_distribute_horizontal(self, nodes: Sequence[FlowNode]) -> None:
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

    def nodes_distribute_vertical(self, nodes: Sequence[FlowNode]) -> None:
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
            name=name,
            dtype=dtype.path,
            docs=None,
            value=dtype.base(),
            initial=dtype.base(),
        )  # type: ignore[var-annotated]
        self.variables.append(result)
        return result
