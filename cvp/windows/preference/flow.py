# -*- coding: utf-8 -*-

import imgui

from cvp.config.sections.canvas.axis import Axis
from cvp.config.sections.canvas.grid import Grid
from cvp.config.sections.flow.logs import Logs
from cvp.config.sections.flow.nodes import Nodes
from cvp.config.sections.flow.pins import Pins
from cvp.imgui.checkbox import checkbox
from cvp.imgui.color_edit4 import color_edit4
from cvp.imgui.combo import combo
from cvp.imgui.input_float import input_float
from cvp.imgui.input_float2 import input_float2
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget


class FlowPreference(PreferenceWidget):
    def __init__(self, context: RendererContext, label="Flow"):
        self._config = context.config.flow_aui
        self._label = label

    @property
    @override
    def label(self) -> str:
        return self._label

    @staticmethod
    def tree_grid(label: str, grid: Grid) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", grid.visible):
                    grid.visible = visible.state
                if step := input_float("Step", grid.step, step=1.0):
                    grid.step = step.value
                if thickness := input_float("Thickness", grid.thickness, step=1.0):
                    grid.thickness = thickness.value
                if color := color_edit4("Color", *grid.color):
                    grid.color = color.color
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_axis(label: str, axis: Axis) -> None:
        if imgui.tree_node(label):
            try:
                if visible := checkbox("Visible", axis.visible):
                    axis.visible = visible
                if thickness := input_float("Thickness", axis.thickness, step=1.0):
                    axis.thickness = thickness.value
                if color := color_edit4("Color", *axis.color):
                    axis.color = color.color
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_logs(label: str, logs: Logs) -> None:
        if not imgui.tree_node(label):
            return

        try:
            if check := checkbox("Autoscroll", logs.autoscroll):
                logs.autoscroll = check.state

            if level := combo("Level", logs.level_index, logs.level_names):
                logs.level_index = level.value

            if filter_text := input_text("Filter", logs.filter):
                logs.filter = filter_text.value

            if lines := input_int("Lines", logs.lines):
                logs.lines = lines.value

            if color := color_edit4("Critical", *logs.critical_color):
                logs.critical_color = color.color
            if color := color_edit4("Error", *logs.error_color):
                logs.error_color = color.color
            if color := color_edit4("Warning", *logs.warning_color):
                logs.warning_color = color.color
            if color := color_edit4("Info", *logs.info_color):
                logs.info_color = color.color
            if color := color_edit4("Debug", *logs.debug_color):
                logs.debug_color = color.color
        finally:
            imgui.tree_pop()

    @staticmethod
    def tree_nodes(label: str, nodes: Nodes) -> None:
        if imgui.tree_node(label):
            try:
                if show_layout := checkbox("Show layout", nodes.show_layout):
                    nodes.show_layout = show_layout.state
                if item_spacing := input_float2("Item spacing", *nodes.item_spacing):
                    nodes.item_spacing = item_spacing.value
            finally:
                imgui.tree_pop()

    @staticmethod
    def tree_pins(label: str, pins: Pins) -> None:
        if imgui.tree_node(label):
            try:
                input_text_disabled("Exec unconnected", pins.exec_n_icon)
                input_text_disabled("Exec connected", pins.exec_y_icon)
                input_text_disabled("Data unconnected", pins.data_n_icon)
                input_text_disabled("Data connected", pins.data_y_icon)
            finally:
                imgui.tree_pop()

    @override
    def on_process(self) -> None:
        self.tree_logs("Logs", self._config.logs)
        self.tree_grid("Grid X", self._config.grid_x)
        self.tree_grid("Grid Y", self._config.grid_x)
        self.tree_axis("Axis X", self._config.axis_x)
        self.tree_axis("Axis Y", self._config.axis_y)
        self.tree_nodes("Nodes", self._config.nodes)
        self.tree_pins("Pins", self._config.pins)
