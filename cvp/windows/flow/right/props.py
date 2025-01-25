# -*- coding: utf-8 -*-

from typing import Final

import imgui

from cvp.config.sections.canvas.axis import Axis
from cvp.flow.arc import FlowArc
from cvp.flow.graph import FlowGraph
from cvp.flow.line_type import (
    LINE_TYPE_INDEX2NAME,
    LINE_TYPE_NAME2INDEX,
    LINE_TYPE_NAMES,
    FlowLineType,
)
from cvp.flow.node import FlowNode
from cvp.flow.pin import FlowPin
from cvp.flow.selection import FlowSelection
from cvp.flow.variable import FlowVariable
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.combo import combo
from cvp.imgui.drag_float2 import drag_float2
from cvp.imgui.input_float import input_float
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_var import style_disable_input
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.canvases import Canvases

INPUT_BUFFER: Final[int] = 256
ENTER_RETURN: Final[int] = imgui.INPUT_TEXT_ENTER_RETURNS_TRUE


class PropsTab(TabItem[Canvases]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Props")

    @override
    def on_item(self, item: Canvases) -> None:
        graph = item.graph
        if graph is None:
            self.on_none()
            return

        selected_items = graph.selection
        selected_nodes = selected_items.nodes
        selected_pins = selected_items.pins
        selected_arcs = selected_items.arcs
        selected_variables = selected_items.variables

        if len(selected_items) == 0:
            self.on_graph_cursor(graph)
        elif len(selected_items) == 1:
            if selected_items.nodes:
                assert 1 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 0 == len(selected_arcs)
                assert 0 == len(selected_variables)
                self.on_node_item(selected_nodes[0])
            elif selected_items.pins:
                assert 0 == len(selected_nodes)
                assert 1 == len(selected_pins)
                assert 0 == len(selected_arcs)
                assert 0 == len(selected_variables)
                self.on_pin_item(selected_pins[0])
            elif selected_items.arcs:
                assert 0 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 1 == len(selected_arcs)
                assert 0 == len(selected_variables)
                self.on_arc_item(graph, selected_arcs[0])
            elif selected_items.variables:
                assert 0 == len(selected_nodes)
                assert 0 == len(selected_pins)
                assert 0 == len(selected_arcs)
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
        input_text_disabled("UUID", graph.uuid)

        graph.name = input_text_value("Name", graph.name)
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

        node.name = input_text_value("Name", node.name)
        node.docs = input_text_value("Docs", node.docs)

        self.input_icon("Icon", node.icon)

        if color_result := color_edit4("Color", *node.color):
            node.color = color_result.color

        if self.context.debug:
            self.tree_node_debugging("Debugging", node)

        # flow_inputs: List[Pin] = field(default_factory=list)
        # flow_outputs: List[Pin] = field(default_factory=list)
        # data_inputs: List[Pin] = field(default_factory=list)
        # data_outputs: List[Pin] = field(default_factory=list)

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
        input_text_disabled("Dtype", pin.dtype)

        with style_disable_input():
            same_vertical_x = 90.0

            imgui.radio_button("Flow", pin.is_flow_action)
            imgui.same_line(same_vertical_x)
            imgui.radio_button("Data", pin.is_data_action)

            imgui.radio_button("Input", pin.is_input_stream)
            imgui.same_line(same_vertical_x)
            imgui.radio_button("Output", pin.is_output_stream)

            imgui.radio_button("Required", pin.required)
            imgui.same_line(same_vertical_x)
            imgui.radio_button("Optional", not pin.required)

        if self.context.debug:
            self.tree_pin_debugging("Debugging", pin)

    def on_arc_item(self, graph: FlowGraph, arc: FlowArc) -> None:
        input_text_disabled("Type", type(arc).__name__)
        input_text_disabled("UUID", arc.uuid)

        arc.name = input_text_value("Name", arc.name)
        arc.docs = input_text_value("Docs", arc.docs)

        line_index = LINE_TYPE_NAME2INDEX[str(arc.line_type)]
        if line_result := combo("Line Type", line_index, LINE_TYPE_NAMES):
            line_name = LINE_TYPE_INDEX2NAME[line_result.value]
            arc.line_type = FlowLineType(line_name)
            graph.update_arc_polyline(arc, force=True)

        sax, say = arc.start_anchor.point
        if anchor_result := drag_float2("Start Anchor", sax, say):
            arc.start_anchor.point = anchor_result.values
            graph.update_arc_polyline(arc, force=True)

        eax, eay = arc.end_anchor.point
        if anchor_result := drag_float2("End Anchor", eax, eay):
            arc.end_anchor.point = anchor_result.values
            graph.update_arc_polyline(arc, force=True)

        if arc.output:
            if imgui.tree_node("Output pin"):
                try:
                    self.on_pin_item(arc.output.pin)
                finally:
                    imgui.tree_pop()

        if arc.input:
            if imgui.tree_node("Input pin"):
                try:
                    self.on_pin_item(arc.input.pin)
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
        input_text_disabled("Name", variable.name)

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
                    elif isinstance(item, FlowArc):
                        self.on_arc_item(graph, item)
                    elif isinstance(item, FlowVariable):
                        self.on_variable_item(item)
                    else:
                        assert False, "Inaccessible section"
                finally:
                    imgui.tree_pop()
