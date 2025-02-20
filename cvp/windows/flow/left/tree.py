# -*- coding: utf-8 -*-

import imgui

from cvp.flow.arc import FlowArc
from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.variable import FlowVariable
from cvp.imgui.drag_types import DRAG_FLOW_VARIABLE
from cvp.imgui.text_centered import text_centered
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.canvases import Canvases

_LEAF = imgui.TREE_NODE_LEAF
_NO_TREE_PUSH_ON_OPEN = imgui.TREE_NODE_NO_TREE_PUSH_ON_OPEN
_OPEN_ON_ARROW = imgui.TREE_NODE_OPEN_ON_ARROW
_OPEN_ON_DOUBLE_CLICK = imgui.TREE_NODE_OPEN_ON_DOUBLE_CLICK
_SPAN_AVAILABLE_WIDTH = imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH

NODE_FLAGS = _OPEN_ON_ARROW | _OPEN_ON_DOUBLE_CLICK | _SPAN_AVAILABLE_WIDTH
PIN_FLAGS = NODE_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN
ARC_FLAGS = NODE_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN
VARIABLE_FLAGS = NODE_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN


class TreeTab(TabItem[Canvases]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Tree")

    @property
    def normal_icon(self):
        return self.context.fonts.normal_icon

    @override
    def on_none(self) -> None:
        text_centered("Please select a graph")

    @override
    def on_item(self, item: Canvases) -> None:
        graph = item.graph
        if graph is None:
            self.on_none()
            return

        graph_label = f"{graph.name}###{graph.uuid}"
        if imgui.tree_node(graph_label, imgui.TREE_NODE_DEFAULT_OPEN):
            try:
                self.tree_nodes(graph)
                self.tree_arcs(graph)
                self.tree_variables(graph)
            finally:
                imgui.tree_pop()

    def tree_nodes(self, graph: FlowGraph) -> None:
        if imgui.tree_node("Nodes"):
            try:
                for node in graph.nodes:
                    self.tree_node(graph, node)
            finally:
                imgui.tree_pop()

    def tree_node(self, graph: FlowGraph, node: FlowNode) -> None:
        flow_pin_n_icon = self.context.config.flow_aui.pins.flow_n_icon
        flow_pin_y_icon = self.context.config.flow_aui.pins.flow_y_icon
        data_pin_n_icon = self.context.config.flow_aui.pins.data_n_icon
        data_pin_y_icon = self.context.config.flow_aui.pins.data_y_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = NODE_FLAGS
        if node.selected:
            flags |= imgui.TREE_NODE_SELECTED

        node_opened = imgui.tree_node(f"{node.name}###{node.uuid}", flags)
        if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
            if not key_ctrl:
                graph.unselect_all_items()
            graph.flip_select_item(node)

        if not node_opened:
            return

        try:
            for pin in node.pins:
                if pin.is_flow_action:
                    pin_icon = flow_pin_y_icon if pin.connected else flow_pin_n_icon
                elif pin.is_data_action:
                    pin_icon = data_pin_y_icon if pin.connected else data_pin_n_icon
                else:
                    assert False, "Inaccessible section"

                flags = PIN_FLAGS
                if pin.selected:
                    flags |= imgui.TREE_NODE_SELECTED

                imgui.tree_node(pin.name, flags)
                if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
                    if not key_ctrl:
                        graph.unselect_all_items()
                    graph.flip_select_item(pin)

                imgui.same_line(imgui.get_cursor_pos_x())

                with self.normal_icon:
                    imgui.text(pin_icon)
        finally:
            imgui.tree_pop()

    def tree_arcs(self, graph: FlowGraph) -> None:
        if imgui.tree_node("Arcs"):
            try:
                for arc in graph.arcs:
                    self.tree_arc(graph, arc)
            finally:
                imgui.tree_pop()

    def tree_arc(self, graph: FlowGraph, arc: FlowArc) -> None:
        arc_n_icon = self.context.config.flow_aui.pins.arc_n_icon
        arc_y_icon = self.context.config.flow_aui.pins.arc_y_icon
        arc_icon = arc_y_icon if arc.selected else arc_n_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = ARC_FLAGS
        if arc.selected:
            flags |= imgui.TREE_NODE_SELECTED

        imgui.tree_node(f"{arc.name}###{arc.uuid}", flags)
        if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
            if not key_ctrl:
                graph.unselect_all_items()
            graph.flip_select_item(arc)

        imgui.same_line(imgui.get_cursor_pos_x())

        with self.normal_icon:
            imgui.text(arc_icon)

    def tree_variables(self, graph: FlowGraph) -> None:
        if imgui.tree_node("Variables"):
            try:
                for variable in graph.variables:
                    self.tree_variable(graph, variable)
            finally:
                imgui.tree_pop()

    def tree_variable(self, graph: FlowGraph, variable: FlowVariable) -> None:
        variable_icon = self.context.config.flow_aui.pins.variable_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = VARIABLE_FLAGS
        if variable.selected:
            flags |= imgui.TREE_NODE_SELECTED

        imgui.tree_node(variable.name, flags)
        if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
            if not key_ctrl:
                graph.unselect_all_items()
            graph.flip_select_item(variable)

        with imgui.begin_drag_drop_source() as drag_drop_src:
            if drag_drop_src.dragging:
                payload = variable.name.encode()
                imgui.set_drag_drop_payload(DRAG_FLOW_VARIABLE, payload)
                imgui.text(variable.name)

        imgui.same_line(imgui.get_cursor_pos_x())

        with self.normal_icon:
            imgui.text(variable_icon)
