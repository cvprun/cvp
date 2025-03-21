# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.flow.graph import FlowGraph
from cvp.flow.node import FlowNode
from cvp.flow.variable import FlowVariable
from cvp.flow.wire import FlowWire
from cvp.imgui.drag_types import DRAG_FLOW_VARIABLE
from cvp.imgui.text_centered import text_centered
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.tab import TabItem

_LEAF = imgui.TREE_NODE_LEAF
_NO_TREE_PUSH_ON_OPEN = imgui.TREE_NODE_NO_TREE_PUSH_ON_OPEN
_OPEN_ON_ARROW = imgui.TREE_NODE_OPEN_ON_ARROW
_OPEN_ON_DOUBLE_CLICK = imgui.TREE_NODE_OPEN_ON_DOUBLE_CLICK
_SPAN_AVAILABLE_WIDTH = imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH
_DEFAULT_OPEN = imgui.TREE_NODE_DEFAULT_OPEN

_COMMON_FLAGS = _OPEN_ON_ARROW | _OPEN_ON_DOUBLE_CLICK | _SPAN_AVAILABLE_WIDTH

CATEGORY_FLAGS = _COMMON_FLAGS | _DEFAULT_OPEN
NODE_FLAGS = _COMMON_FLAGS
PIN_FLAGS = _COMMON_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN
ARC_FLAGS = _COMMON_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN
VARIABLE_FLAGS = _COMMON_FLAGS | _LEAF | _NO_TREE_PUSH_ON_OPEN


class TreeTab(TabItem[FlowCanvasTabs]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Tree")

    @property
    def normal_icon(self):
        return self.context.fonts.normal_icon

    @override
    def on_none(self) -> None:
        text_centered("Please select a graph")

    @override
    def on_item(self, item: FlowCanvasTabs) -> None:
        graph = item.graph
        if graph is None:
            self.on_none()
            return

        graph_label = f"{graph.name}###{graph.key}"
        if imgui.tree_node(graph_label, CATEGORY_FLAGS):
            try:
                self.tree_nodes(graph)
                self.tree_wires(graph)
                self.tree_variables(graph)
            finally:
                imgui.tree_pop()

    def tree_nodes(self, graph: FlowGraph) -> None:
        if imgui.tree_node("Nodes", CATEGORY_FLAGS):
            try:
                for node in graph.nodes:
                    self.tree_node(graph, node)
            finally:
                imgui.tree_pop()

    def tree_node(self, graph: FlowGraph, node: FlowNode) -> None:
        exec_pin_n_icon = self.context.config.flow_aui.pins.exec_n_icon
        exec_pin_y_icon = self.context.config.flow_aui.pins.exec_y_icon
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
                if pin.is_exec_action:
                    pin_icon = exec_pin_y_icon if pin.connected else exec_pin_n_icon
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

    def tree_wires(self, graph: FlowGraph) -> None:
        if imgui.tree_node("Wires", CATEGORY_FLAGS):
            try:
                for wire in graph.wires:
                    self.tree_wire(graph, wire)
            finally:
                imgui.tree_pop()

    def tree_wire(self, graph: FlowGraph, wire: FlowWire) -> None:
        wire_n_icon = self.context.config.flow_aui.pins.wire_n_icon
        wire_y_icon = self.context.config.flow_aui.pins.wire_y_icon
        wire_icon = wire_y_icon if wire.connected else wire_n_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = ARC_FLAGS
        if wire.selected:
            flags |= imgui.TREE_NODE_SELECTED

        imgui.tree_node(f"{wire.name}###{wire.uuid}", flags)
        if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
            if not key_ctrl:
                graph.unselect_all_items()
            graph.flip_select_item(wire)

        imgui.same_line(imgui.get_cursor_pos_x())

        with self.normal_icon:
            imgui.text(wire_icon)

    def tree_variables(self, graph: FlowGraph) -> None:
        if imgui.tree_node("Variables", CATEGORY_FLAGS):
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

        label = f"({variable.dtype.class_name}) {variable.name}"
        imgui.tree_node(label, flags)

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
