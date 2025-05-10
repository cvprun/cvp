# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui

from cvp.apps.player.widgets.flows.drag_types import DRAG_FLOW_GRAPH
from cvp.flow.graph import FlowGraph
from cvp.imgui.drag_drop import begin_source, end_source, set_payload
from cvp.imgui.flags.cond import Cond
from cvp.imgui.flags.mouse_button import MOUSE_LEFT, MouseButton
from cvp.imgui.flags.selectable import ALLOW_DOUBLE_CLICK, SelectableFlags
from cvp.imgui.selectable import SelectableResult, selectable


def drag_graph_source(graph: FlowGraph, cond: Union[Cond, int] = 0):
    if begin_source():
        try:
            set_payload(DRAG_FLOW_GRAPH, graph.key, cond)
            imgui.text(graph.name if graph.name else FlowGraph.__name__)
        finally:
            end_source()


def selectable_graph(
    graph: FlowGraph,
    selected=False,
    flags: Union[SelectableFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
    *,
    use_drag_source=False,
    drag_cond: Union[Cond, int] = 0,
    use_double_clicked=False,
    double_click_button: Union[MouseButton, int] = MOUSE_LEFT,
):
    if isinstance(flags, SelectableFlags):
        flags = int(flags)
    assert isinstance(flags, int)

    if use_double_clicked:
        flags |= ALLOW_DOUBLE_CLICK

    name = str(graph.name) if graph.name else FlowGraph.__name__
    label = f"{name}###{graph.uuid}"
    result = selectable(label, selected, flags, size)

    if result.clicked and use_double_clicked:
        if isinstance(double_click_button, MouseButton):
            double_click_button = int(double_click_button)
        assert isinstance(double_click_button, int)

        clicked = imgui.is_mouse_double_clicked(double_click_button)
        result = SelectableResult(clicked, result.selected)

    if use_drag_source:
        drag_graph_source(graph, drag_cond)

    return result
