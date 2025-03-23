# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.config.sections.canvas.axis import Axis
from cvp.flow.graph import FlowGraph, GraphName
from cvp.flow.line_type import (
    LINE_TYPE_INDEX2NAME,
    LINE_TYPE_NAME2INDEX,
    LINE_TYPE_NAMES,
    FlowLineType,
)
from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin
from cvp.flow.selection import FlowSelection
from cvp.flow.variable import FlowVariable, VariableName
from cvp.flow.wire import FlowWire
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.combo import combo
from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.input_dtype import input_dtype
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_var import style_disable_input
from cvp.nodes.node import NodeName
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.tab import TabItem


class PropsTab(TabItem[FlowCanvasTabs]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Props")

    @override
    def on_item(self, item: FlowCanvasTabs) -> None:
        graph = item.graph
        if graph is None:
            self.on_none()
            return

        selected_items = graph.selection
        selected_nodes = selected_items.nodes
        selected_pins = selected_items.pins
        selected_wires = selected_items.wires
        selected_variables = selected_items.variables

        if len(selected_items) == 0:
            self.on_graph_cursor(graph)
        elif len(selected_items) == 1:
            if selected_items.nodes:
                assert 1 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 0 == len(selected_wires)
                assert 0 == len(selected_variables)
                self.on_node_item(selected_nodes[0])
            elif selected_items.pins:
                assert 0 == len(selected_nodes)
                assert 1 == len(selected_pins)
                assert 0 == len(selected_wires)
                assert 0 == len(selected_variables)
                self.on_pin_item(selected_pins[0])
            elif selected_items.wires:
                assert 0 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 1 == len(selected_wires)
                assert 0 == len(selected_variables)
                self.on_wire_item(graph, selected_wires[0])
            elif selected_items.variables:
                assert 0 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 0 == len(selected_wires)
                assert 1 == len(selected_variables)
                self.on_variable_item(selected_variables[0])
            else:
                assert False, "Inaccessible section"
        else:
            assert 2 <= len(selected_items)
            self.on_multiple_items(graph, selected_items)

    def input_icon(self, label: str, icon: str) -> None:
        with self.context.fonts.normal_icon:
            input_text_disabled(f"##{label}", icon)
        imgui.same_line(0.0, imgui.get_style().item_inner_spacing[0])
        imgui.text(label)

    @staticmethod
    def tree_axis(label: str, axis: Axis) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", axis.visible):
                    axis.visible = visible
                if thickness := input_float("Thickness", axis.thickness):
                    axis.thickness = thickness.value
                if color := color_edit4("Color", *axis.color):
                    axis.color = color.color
            finally:
                imgui.tree_pop()

    def on_graph_cursor(self, graph: FlowGraph) -> None:
        input_text_disabled("Type", "Graph")
        input_text_disabled("UUID", graph.key)

        graph.name = GraphName(input_text_value("Name", graph.name))
        graph.docs = input_text_value("Docs", graph.docs)

        self.input_icon("Icon", graph.icon)

    @staticmethod
    def tree_node_debugging(label: str, node: FlowNode) -> None:
        if imgui.tree_node(label):
            try:
                message = node.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def on_node_item(self, node: FlowNode) -> None:
        input_text_disabled("Type", type(node).__name__)
        input_text_disabled("UUID", node.uuid)

        node.name = NodeName(input_text_value("Name", node.name))
        node.docs = input_text_value("Docs", node.docs)

        self.input_icon("Icon", node.icon)

        if lock := checkbox("Lock", node.lock):
            node.lock = lock.state
        if bp := checkbox("Breakpoint", node.breakpoint):
            node.breakpoint = bp.state
        if hidden := checkbox("Hidden", node.hidden):
            node.hidden = hidden.state

        if color_result := color_edit4("Color", *node.color):
            node.color = color_result.color

        # if template := self.context.fm.nodes.get(node.path):
        #     template.on_render_properties()

        if self.context.debug:
            self.tree_node_debugging("Debugging", node)

    @staticmethod
    def tree_pin_debugging(label: str, pin: FlowPin) -> None:
        if imgui.tree_node(label):
            try:
                message = pin.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def on_pin_item(self, pin: FlowPin) -> None:
        input_text_disabled("Type", type(pin).__name__)
        input_text_disabled("Name", pin.name)
        input_text_disabled("Docs", pin.docs)
        input_text_disabled("Dtype", pin.dtype.path)

        with style_disable_input():
            same_vertical_x = 90.0

            imgui.radio_button("Flow", pin.is_exec_action)
            imgui.same_line(same_vertical_x)
            imgui.radio_button("Data", pin.is_data_action)

            imgui.radio_button("Input", pin.is_input_stream)
            imgui.same_line(same_vertical_x)
            imgui.radio_button("Output", pin.is_output_stream)

            imgui.radio_button("Required", pin.required)
            imgui.same_line(same_vertical_x)
            imgui.radio_button("Optional", not pin.required)

            imgui.radio_button("Hidden", pin.hidden)
            imgui.same_line(same_vertical_x)
            imgui.radio_button("Visible", not pin.hidden)

        if pin.is_data_inputs:
            if default := input_dtype("Default", pin.default, pin.dtype):
                pin.default = default.value

        if self.context.debug:
            self.tree_pin_debugging("Debugging", pin)

    def on_wire_item(self, graph: FlowGraph, wire: FlowWire) -> None:
        input_text_disabled("Type", type(wire).__name__)
        input_text_disabled("UUID", wire.uuid)

        wire.name = input_text_value("Name", wire.name)
        wire.docs = input_text_value("Docs", wire.docs)

        line_index = LINE_TYPE_NAME2INDEX[str(wire.line_type)]
        if line_result := combo("Line Type", line_index, LINE_TYPE_NAMES):
            line_name = LINE_TYPE_INDEX2NAME[line_result.value]
            wire.line_type = FlowLineType(line_name)
            graph.update_wire_polyline(wire, force=True)

        sax, say = wire.start_anchor.point
        if anchor_result := drag_float2("Start Anchor", sax, say):
            wire.start_anchor.point = anchor_result.values
            graph.update_wire_polyline(wire, force=True)

        eax, eay = wire.end_anchor.point
        if anchor_result := drag_float2("End Anchor", eax, eay):
            wire.end_anchor.point = anchor_result.values
            graph.update_wire_polyline(wire, force=True)

        if wire.output:
            if imgui.tree_node("Output pin"):
                try:
                    self.on_pin_item(wire.output.pin)
                finally:
                    imgui.tree_pop()

        if wire.input:
            if imgui.tree_node("Input pin"):
                try:
                    self.on_pin_item(wire.input.pin)
                finally:
                    imgui.tree_pop()

    @staticmethod
    def tree_variable_debugging(label: str, variable: FlowVariable) -> None:
        if imgui.tree_node(label):
            try:
                message = variable.as_unformatted_text()
                imgui.text_unformatted(message.strip())
            finally:
                imgui.tree_pop()

    def on_variable_item(self, variable: FlowVariable) -> None:
        input_text_disabled("Type", type(variable).__name__)
        input_text_disabled("Dtype", variable.dtype.path)

        variable.name = VariableName(input_text_value("Name", variable.name))
        variable.docs = input_text_value("Docs", variable.docs)

        if imgui.radio_button("Persistent", variable.persistent):
            variable.persistent = True
        imgui.same_line()
        if imgui.radio_button("Temporary", not variable.persistent):
            variable.persistent = False

        if imgui.radio_button("Assign", variable.is_assign_method):
            variable.use_copy = False
            variable.use_deepcopy = False
        imgui.same_line()
        if imgui.radio_button("Copy", variable.use_copy):
            variable.use_copy = True
            variable.use_deepcopy = False
        imgui.same_line()
        if imgui.radio_button("Deepcopy", variable.use_deepcopy):
            variable.use_copy = False
            variable.use_deepcopy = True

        if initial := input_dtype("Initial", variable.initial, variable.dtype):
            variable.initial = initial.value

        if value := input_dtype("Value", variable.value, variable.dtype):
            variable.value = value.value

        if self.context.debug:
            self.tree_variable_debugging("Debugging", variable)

    def on_multiple_items(self, graph: FlowGraph, items: FlowSelection) -> None:
        input_text_disabled("Type", "Multiple")

        for key, item in items.items():
            typename = type(item).__name__
            title = f"{typename} ({item.name})" if item.name else typename
            label = f"{title}###{key}"

            if imgui.tree_node(label):
                try:
                    if isinstance(item, FlowNode):
                        self.on_node_item(item)
                    elif isinstance(item, FlowPin):
                        self.on_pin_item(item)
                    elif isinstance(item, FlowWire):
                        self.on_wire_item(graph, item)
                    elif isinstance(item, FlowVariable):
                        self.on_variable_item(item)
                    else:
                        assert False, "Inaccessible section"
                finally:
                    imgui.tree_pop()
