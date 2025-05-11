# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.apps.player.widgets.flows.selectable_variable import drag_variable_source
from cvp.context.context import Context
from cvp.flow.graph import FlowGraph, GraphKey
from cvp.flow.node import FlowNode
from cvp.flow.variable import FlowVariable
from cvp.flow.wire import FlowWire
from cvp.imgui.flags.tree_node import (
    ARC_FLAGS,
    CATEGORY_FLAGS,
    NODE_FLAGS,
    PIN_FLAGS,
    SELECTED,
    VARIABLE_FLAGS,
)
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class TreeFlowWindow(BaseWindow):
    __cvp_window_name__ = "Tree"
    __cvp_window_position__ = DockPosition.left_top

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def focused_graph(self):
        return self.context.flows.graphs.get(GraphKey(self.focused_key))

    @override
    def on_main_process(self) -> None:
        if graph := self.focused_graph:
            self.do_child_process(graph)
        else:
            text_centered("Please select a graph")

    def do_child_process(self, graph: FlowGraph) -> None:
        graph_label = f"{graph.name}###{graph.key}"
        if imgui.tree_node_ex(graph_label, CATEGORY_FLAGS):
            try:
                self.tree_nodes(graph)
                self.tree_wires(graph)
                self.tree_variables(graph)
            finally:
                imgui.tree_pop()

    def tree_nodes(self, graph: FlowGraph) -> None:
        if imgui.tree_node_ex("Nodes", CATEGORY_FLAGS):
            try:
                for node in graph.nodes:
                    self.tree_node(graph, node)
            finally:
                imgui.tree_pop()

    def tree_node(self, graph: FlowGraph, node: FlowNode) -> None:
        exec_pin_n_icon = self.context.config.flow.pins.exec_n_icon
        exec_pin_y_icon = self.context.config.flow.pins.exec_y_icon
        data_pin_n_icon = self.context.config.flow.pins.data_n_icon
        data_pin_y_icon = self.context.config.flow.pins.data_y_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = NODE_FLAGS
        if node.selected:
            flags |= SELECTED

        node_opened = imgui.tree_node_ex(f"{node.name}###{node.uuid}", flags)
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
                    flags |= SELECTED

                imgui.tree_node_ex(pin.name, flags)
                if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
                    if not key_ctrl:
                        graph.unselect_all_items()
                    graph.flip_select_item(pin)

                imgui.same_line(imgui.get_cursor_pos_x())

                if True:  # with self.normal_icon:
                    imgui.text(pin_icon)
        finally:
            imgui.tree_pop()

    def tree_wires(self, graph: FlowGraph) -> None:
        if imgui.tree_node_ex("Wires", CATEGORY_FLAGS):
            try:
                for wire in graph.wires:
                    self.tree_wire(graph, wire)
            finally:
                imgui.tree_pop()

    def tree_wire(self, graph: FlowGraph, wire: FlowWire) -> None:
        wire_n_icon = self.context.config.flow.pins.wire_n_icon
        wire_y_icon = self.context.config.flow.pins.wire_y_icon
        wire_icon = wire_y_icon if wire.connected else wire_n_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = ARC_FLAGS
        if wire.selected:
            flags |= SELECTED

        imgui.tree_node_ex(f"{wire.name}###{wire.uuid}", flags)
        if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
            if not key_ctrl:
                graph.unselect_all_items()
            graph.flip_select_item(wire)

        imgui.same_line(imgui.get_cursor_pos_x())

        if True:  # with self.normal_icon:
            imgui.text(wire_icon)

    def tree_variables(self, graph: FlowGraph) -> None:
        if imgui.tree_node_ex("Variables", CATEGORY_FLAGS):
            try:
                for variable in graph.variables:
                    self.tree_variable(graph, variable)
            finally:
                imgui.tree_pop()

    def tree_variable(self, graph: FlowGraph, variable: FlowVariable) -> None:
        variable_icon = self.context.config.flow.pins.variable_icon
        key_ctrl = imgui.get_io().key_ctrl

        flags = VARIABLE_FLAGS
        if variable.selected:
            flags |= SELECTED

        label = f"({variable.dtype.class_name}) {variable.key}"
        imgui.tree_node_ex(label, flags)

        if imgui.is_item_clicked() and not imgui.is_item_toggled_open():
            if not key_ctrl:
                graph.unselect_all_items()
            graph.flip_select_item(variable)

        drag_variable_source(variable)

        imgui.same_line(imgui.get_cursor_pos_x())

        if True:  # with self.normal_icon:
            imgui.text(variable_icon)
