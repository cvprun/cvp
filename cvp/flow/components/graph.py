# -*- coding: utf-8 -*-

from copy import deepcopy
from dataclasses import dataclass, field
from functools import reduce
from math import sqrt
from typing import List, Optional, Sequence, Set, Union
from uuid import uuid4

import shapely

from cvp.flow.components.action import Action
from cvp.flow.components.anchor import Anchor
from cvp.flow.components.arc import Arc
from cvp.flow.components.connection import Connection
from cvp.flow.components.control import Control
from cvp.flow.components.node import Node
from cvp.flow.components.node_pin import NodePin
from cvp.flow.components.pin import Pin
from cvp.flow.components.selection import SelectableAny, Selection
from cvp.flow.components.stream import Stream
from cvp.templates.graph import GraphTemplate
from cvp.types.colors import RGBA, WHITE_RGBA
from cvp.types.shapes import Point, Size


@dataclass
class Graph:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = str()
    docs: str = str()
    icon: str = str()
    lock: bool = False
    color: RGBA = WHITE_RGBA
    nodes: List[Node] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    control: Control = field(default_factory=Control)

    _selection: Selection = field(default_factory=Selection)
    _template: Optional[GraphTemplate] = None

    @classmethod
    def from_template(cls, template: GraphTemplate):
        return cls(
            uuid=str(uuid4()),
            name=template.name,
            docs=template.docs,
            icon=template.icon,
            color=template.color,
            nodes=list(Node.from_template(n) for n in template.nodes),
            tags=deepcopy(template.tags),
            arcs=list(),  # TODO ...
            _template=template,
        )

    @property
    def template(self):
        return self._template

    @property
    def selection(self):
        return self._selection

    @property
    def selected_arc_only(self) -> Optional[Arc]:
        return self._selection.selected_arc_only

    def restore(self, other: "Graph") -> None:
        if self.uuid != other.uuid:
            raise ValueError("The uuid of the graph to be restored does not match")

        self.name = other.name
        self.docs = other.docs
        self.icon = other.icon
        self.nodes = other.nodes
        self.arcs = other.arcs
        self.control = other.control
        self._selection = other._selection

    def paste_selection(
        self,
        items: Selection,
        point: Point,
        *,
        selected: Optional[bool] = None,
    ) -> None:
        nodes, arcs = items.copy_validated_items(point)

        if selected is not None:
            for node in nodes:
                for pin in node.pins:
                    pin.selected = False
                node.selected = selected
            for arc in arcs:
                arc.selected = selected

        for node in nodes:
            self.nodes.insert(0, node)
        for arc in arcs:
            self.arcs.insert(0, arc)

        self.update_selected_items()
        self.update_arcs_polyline(force=True)

    def update_selected_item(self, item: SelectableAny) -> None:
        self._selection.apply(item)

    def update_selected_items(self) -> None:
        for node in self.nodes:
            for pin in node.pins:
                self._selection.apply(pin)
            self._selection.apply(node)
        for arc in self.arcs:
            self._selection.apply(arc)

    def update_selected_nodes(self) -> None:
        for node in self.nodes:
            self._selection.apply(node)

    def update_selected_arcs(self) -> None:
        for arc in self.arcs:
            self._selection.apply(arc)

    def select_item(self, item: SelectableAny, *, selected=True) -> None:
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

    def unselect_item(self, item: SelectableAny) -> None:
        self.select_item(item, selected=False)

    def flip_select_item(self, item: SelectableAny) -> None:
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

    def find_hovering_node_with_mouse(self, mouse: Point) -> Optional[Node]:
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

    def find_hovering_node(self) -> Optional[Node]:
        for node in self.nodes:
            if node.hovering:
                return node
        return None

    def find_hovering_pin(self) -> Optional[NodePin]:
        node = self.find_hovering_node()
        if node is None:
            return None

        if not node.hovering:
            raise ValueError("Only hovering nodes are allowed")

        pin = node.find_hovering_pin()
        if pin is None:
            return None

        return NodePin(node, pin)

    def find_hovering_arc_with_mouse(self, mouse: Point) -> Optional[Arc]:
        mp = shapely.Point(mouse)
        for arc in self.arcs:
            distance = shapely.LineString(arc.polyline).distance(mp)
            if distance <= self.control.arc_hovering_tolerance:
                return arc
        return None

    def find_hovering_arc(self) -> Optional[Arc]:
        for arc in self.arcs:
            if arc.hovering:
                return arc
        return None

    def find_hovering_anchor_with_mouse(
        self,
        arc: Arc,
        mouse: Point,
    ) -> Optional[Anchor]:
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

    def find_hovering_anchor(self) -> Optional[Anchor]:
        if selected_arc := self.selected_arc_only:
            if selected_arc.start_anchor.hovering:
                return selected_arc.start_anchor
            if selected_arc.end_anchor.hovering:
                return selected_arc.end_anchor
        return None

    def find_hovering_item(self) -> Optional[Union[Node, Pin, Arc]]:
        if node := self.find_hovering_node():
            assert node.hovering

            if pin := node.find_hovering_pin():
                assert pin.hovering
                return pin

            return node

        if arc := self.find_hovering_arc():
            assert arc.hovering
            return arc

        return None

    def find_arc(self, arc_uuid: str) -> Optional[Arc]:
        for arc in self.arcs:
            if arc.uuid == arc_uuid:
                return arc
        return None

    def pop_arcs(self, uuids: Union[Set[str], Sequence[str]]) -> List[Arc]:
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

    def find_selected_arcs(self) -> List[Arc]:
        result = list()
        for arc in self.arcs:
            if arc.selected:
                result.append(arc)
        return result

    def find_selected_pins(self) -> List[Pin]:
        result = list()
        for node in self.nodes:
            result.extend(node.find_selected_pins())
        return result

    def find_selected_nodes(self) -> List[Node]:
        result = list()
        for node in self.nodes:
            if node.selected:
                result.append(node)
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

        self._selection.clear()

    def flip_selected_on_hovering_item(self) -> Optional[Union[Node, Pin, Arc]]:
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

        return None

    def move_node(self, node: Node, pos: Point) -> None:
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

    def update_arc_io(self, arc: Arc, *, force=False) -> None:
        self.update_arc_output(arc, force=force)
        self.update_arc_input(arc, force=force)

    def update_arc_output(self, arc: Arc, *, force=False) -> None:
        if not force and arc.output is not None:
            return

        for node in self.nodes:
            if pin := node.find_output_pin(arc.uuid):
                arc.output = NodePin(node, pin)
                return

        raise IndexError("Could not find the output pin of the arc")

    def update_arc_input(self, arc: Arc, *, force=False) -> None:
        if not force and arc.input is not None:
            return

        for node in self.nodes:
            if pin := node.find_input_pin(arc.uuid):
                arc.input = NodePin(node, pin)
                return

        raise IndexError("Could not find the input pin of the arc")

    @staticmethod
    def reorder_connectable_pins(left: NodePin, right: NodePin) -> Connection:
        if left.node == right.node:
            raise ValueError("Identical nodes cannot be connected")
        if left.pin.stream == right.pin.stream:
            raise ValueError("Identical streams cannot be connected")
        if left.pin.action != right.pin.action:
            raise ValueError("The action of the pins must match")
        if left.pin.dtype != right.pin.dtype:
            raise ValueError("The dtype of the pins must match")

        if left.pin.stream == Stream.input:
            assert right.pin.stream == Stream.output
            out_conn = right
            in_conn = left
        else:
            assert left.pin.stream == Stream.output
            assert right.pin.stream == Stream.input
            out_conn = left
            in_conn = right

        out_pin = out_conn.pin
        in_pin = in_conn.pin
        assert out_pin.stream == Stream.output
        assert in_pin.stream == Stream.input
        assert out_pin.action == in_pin.action
        action = in_pin.action

        if action == Action.flow and out_pin.arcs:
            raise ValueError("There cannot be multiple output flow pins")
        if action == Action.data and in_pin.arcs:
            raise ValueError("There cannot be multiple input data pins")

        return Connection(out_conn, in_conn)

    @staticmethod
    def is_connectable_pins(left: NodePin, right: NodePin) -> bool:
        try:
            Graph.reorder_connectable_pins(left, right)
        except ValueError:
            return False
        else:
            return True

    def update_arcs_polyline(self, *, force=False) -> None:
        for arc in self.arcs:
            self.update_arc_polyline(arc, force=force)

    def update_arc_polyline(self, arc: Arc, *, force=False) -> None:
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
        out_conn: NodePin,
        in_conn: NodePin,
        *,
        no_reorder=False,
    ) -> Arc:
        if not no_reorder:
            out_conn, in_conn = self.reorder_connectable_pins(out_conn, in_conn)

        arc = Arc.from_connect_pair(
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

    def remove_arc(self, arc: Arc) -> None:
        if arc.input:
            arc.input.pin.arcs.remove(arc.uuid)
        if arc.output:
            arc.output.pin.arcs.remove(arc.uuid)
        self.arcs.remove(arc)
        self._selection.remove_noraise(arc)

    def remove_selected_arcs(self) -> None:
        for arc in self.find_selected_arcs():
            self.remove_arc(arc)

    def remove_node(self, node: Node):
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

    def items_to_front(self, items: Sequence[SelectableAny]) -> None:
        for item in items:
            self.item_to_front(item)

    def item_to_front(self, item: SelectableAny) -> None:
        if isinstance(item, Node):
            self.node_to_front(item)
        elif isinstance(item, Arc):
            self.arc_to_front(item)
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_to_front(self, node: Node) -> None:
        index = self.nodes.index(node)
        if 0 <= index - 1:
            assert node == self.nodes.pop(index)
            self.nodes.insert(index - 1, node)

    def arc_to_front(self, arc: Arc) -> None:
        index = self.arcs.index(arc)
        if 0 <= index - 1:
            assert arc == self.arcs.pop(index)
            self.arcs.insert(index - 1, arc)

    def items_to_back(self, items: Sequence[SelectableAny]) -> None:
        for item in items:
            self.item_to_back(item)

    def item_to_back(self, item: SelectableAny) -> None:
        if isinstance(item, Node):
            self.node_to_back(item)
        elif isinstance(item, Arc):
            self.arc_to_back(item)
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_to_back(self, node: Node) -> None:
        index = self.nodes.index(node)
        if index + 1 < len(self.nodes):
            assert node == self.nodes.pop(index)
            self.nodes.insert(index + 1, node)

    def arc_to_back(self, arc: Arc) -> None:
        index = self.arcs.index(arc)
        if index + 1 < len(self.arcs):
            assert arc == self.arcs.pop(index)
            self.arcs.insert(index + 1, arc)

    def item_bring_forward(self, item: SelectableAny) -> None:
        if isinstance(item, Node):
            self.node_bring_forward(item)
        elif isinstance(item, Arc):
            self.arc_bring_forward(item)
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_bring_forward(self, node: Node) -> None:
        index = self.nodes.index(node)
        if 0 != index:
            assert node == self.nodes.pop(index)
            self.nodes.insert(0, node)

    def arc_bring_forward(self, arc: Arc) -> None:
        index = self.arcs.index(arc)
        if 0 != index:
            assert arc == self.arcs.pop(index)
            self.arcs.insert(0, arc)

    def item_send_backward(self, item: SelectableAny) -> None:
        if isinstance(item, Node):
            self.node_send_backward(item)
        elif isinstance(item, Arc):
            self.arc_send_backward(item)
        else:
            raise TypeError(f"Unsupported item type: {type(item).__name__}")

    def node_send_backward(self, node: Node) -> None:
        index = self.nodes.index(node)
        if index < len(self.arcs) - 1:
            assert node == self.nodes.pop(index)
            self.nodes.append(node)

    def arc_send_backward(self, arc: Arc) -> None:
        index = self.arcs.index(arc)
        if index < len(self.arcs) - 1:
            assert arc == self.arcs.pop(index)
            self.arcs.append(arc)

    def nodes_align_left(self, nodes: Sequence[Node], pivot: Node) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            px, py = pivot.node_pos
            next_pox = px, ny
            self.move_node(node, next_pox)

    def nodes_align_center(self, nodes: Sequence[Node], pivot: Node) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = px + (pw / 2) - (nw / 2), ny
            self.move_node(node, next_pos)

    def nodes_align_right(self, nodes: Sequence[Node], pivot: Node) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = px + pw - nw, ny
            self.move_node(node, next_pos)

    def nodes_align_top(self, nodes: Sequence[Node], pivot: Node) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            px, py = pivot.node_pos
            next_pox = nx, py
            self.move_node(node, next_pox)

    def nodes_align_middle(self, nodes: Sequence[Node], pivot: Node) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = nx, py + (ph / 2) - (nh / 2)
            self.move_node(node, next_pos)

    def nodes_align_bottom(self, nodes: Sequence[Node], pivot: Node) -> None:
        for node in nodes:
            nx, ny = node.node_pos
            nw, nh = node.node_size
            px, py = pivot.node_pos
            pw, ph = pivot.node_size
            next_pos = nx, py + ph - nh
            self.move_node(node, next_pos)

    def nodes_distribute_horizontal(self, nodes: Sequence[Node]) -> None:
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

    def nodes_distribute_vertical(self, nodes: Sequence[Node]) -> None:
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
