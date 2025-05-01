# -*- coding: utf-8 -*-

from typing import Optional, Union

from imgui_bundle import imgui

from cvp.apps.player.widgets.flows.drag_types import DRAG_FLOW_DTYPE
from cvp.dtypes.dtype import Dtype
from cvp.imgui.drag_drop import begin_source, end_source, set_payload
from cvp.imgui.flags.cond import Cond
from cvp.imgui.flags.selectable import SelectableFlags
from cvp.imgui.selectable import selectable


def drag_dtype_source(dtype: Dtype, cond: Union[Cond, int] = 0):
    if begin_source():
        try:
            set_payload(DRAG_FLOW_DTYPE, dtype.path, cond)
            imgui.text(dtype.path)
        finally:
            end_source()


def selectable_dtype(
    dtype: Dtype,
    selected=False,
    flags: Union[SelectableFlags, int] = 0,
    size: Optional[imgui.ImVec2Like] = None,
    *,
    use_drag_source=False,
    drag_cond: Union[Cond, int] = 0,
):
    result = selectable(dtype.path, selected, flags, size)
    if use_drag_source:
        drag_dtype_source(dtype, drag_cond)
    return result
