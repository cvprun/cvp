# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui

from cvp.apps.player.widgets.flows.drag_types import DRAG_FLOW_VARIABLE
from cvp.flow.variable import FlowVariable
from cvp.imgui.drag_drop import begin_source, end_source, set_payload
from cvp.imgui.flags.cond import Cond
from cvp.imgui.flags.selectable import SelectableFlags
from cvp.imgui.selectable import selectable


def drag_variable_source(variable: FlowVariable, cond: Union[Cond, int] = 0):
    if begin_source():
        try:
            set_payload(DRAG_FLOW_VARIABLE, variable.key, cond)
            imgui.text(variable.key)
        finally:
            end_source()


def selectable_variable(
    variable: FlowVariable,
    selected=False,
    flags: Union[SelectableFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
    *,
    use_drag_source=False,
    drag_cond: Union[Cond, int] = 0,
):
    result = selectable(variable.key, selected, flags, size)
    if use_drag_source:
        drag_variable_source(variable, drag_cond)
    return result
