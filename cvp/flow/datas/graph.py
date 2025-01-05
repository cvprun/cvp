# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from math import sqrt
from typing import List, Optional, Sequence, Set, Union
from uuid import uuid4

import shapely

from cvp.flow.datas.action import Action
from cvp.flow.datas.anchor import Anchor
from cvp.flow.datas.arc import Arc
from cvp.flow.datas.connect_pair import ConnectPair
from cvp.flow.datas.control import Control
from cvp.flow.datas.node import Node
from cvp.flow.datas.node_pin import NodePin
from cvp.flow.datas.pin import Pin
from cvp.flow.datas.selected_items import SelectableAny, SelectedItems
from cvp.flow.datas.stream import Stream
from cvp.types.shapes import Point, Size


@dataclass
class Graph:
    uuid: str = field(default_factory=lambda: str(uuid4()))
    name: str = str()
    docs: str = str()
    icon: str = str()
    nodes: List[Node] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    control: Control = field(default_factory=Control)

    _selected_items: SelectedItems = field(default_factory=SelectedItems)

    def restore(self, other: "Graph") -> None:
        if self.uuid != other.uuid:
            raise ValueError("The uuid of the graph to be restored does not match")

        self.name = other.name
        self.docs = other.docs
        self.icon = other.icon
        self.nodes = other.nodes
        self.arcs = other.arcs
        self.control = other.control
        self._selected_items = other._selected_items

    @property
    def selected_items(self):
        return self._selected_items

    @property
    def selected_arc_only(self) -> Optional[Arc]:
        return self._selected_items.selected_arc_only

    def update_selected_item(self, item: SelectableAny) -> None:
        self._selected_items.apply(item)

    def update_selected_nodes(self) -> None:
        for node in self.nodes:
            self._selected_items.apply(node)

    def select_item(self, item: SelectableAny, *, selected=True) -> None:
        item.selected = selected
        if selected:
            self._selected_items.add(item)
        else:
            self._selected_items.remove(item)

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

        self._selected_items.clear()

    def flip_selected_on_hovering_item(self) -> Optional[Union[Node, Pin, Arc]]:
        if node := self.find_hovering_node():
            assert node.hovering

            if pin := node.find_hovering_pin():
                assert pin.hovering
                pin.selected = not pin.selected
                self._selected_items.apply(pin)
                return pin
            else:
                node.selected = not node.selected
                self._selected_items.apply(node)
                return node

        if arc := self.find_hovering_arc():
            assert arc.hovering
            arc.selected = not arc.selected
            self._selected_items.apply(arc)
            return arc

        return None

    def move_on_selected_nodes(self, delta: Size) -> None:
        dx, dy = delta
        if dx == 0 and dy == 0:
            return

        for node in self.nodes:
            if not node.selected:
                continue

            x, y = node.node_pos
            node.node_pos = x + dx, y + dy

            for pin in node.pins:
                for arc_uuid in pin.arcs:
                    if arc := self.find_arc(arc_uuid):
                        self.update_arc_polyline(arc, force=True)

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
    def reorder_connectable_pins(left: NodePin, right: NodePin) -> ConnectPair:
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

        return ConnectPair(out_conn, in_conn)

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

    def remove_selected_arcs(self) -> None:
        for arc in self.find_selected_arcs():
            self.remove_arc(arc)

    def remove_node(self, node: Node):
        for pin in node.pins:
            for arc_uuid in pin.arcs:
                if arc := self.find_arc(arc_uuid):
                    self.remove_arc(arc)
        self.nodes.remove(node)

    def remove_selected_nodes(self) -> None:
        for node in self.find_selected_nodes():
            self.remove_node(node)

    def remove_selected_items(self) -> None:
        self.remove_selected_arcs()
        self.remove_selected_nodes()
        self._selected_items.clear()
