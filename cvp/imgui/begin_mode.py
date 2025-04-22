# -*- coding: utf-8 -*-

from contextlib import contextmanager
from typing import Optional, Union

from imgui_bundle import imgui

from cvp.imgui.begin import begin, end
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS, WindowFlags


@contextmanager
def begin_mode_context(
    label: str,
    closable: Optional[bool] = None,
    flags: Union[WindowFlags, int] = ROOT_STATIC_VIEWPORT_FLAGS,
    viewport: Optional[imgui.Viewport] = None,
):
    viewport = viewport if viewport else imgui.get_main_viewport()
    assert viewport is not None
    imgui.set_next_window_pos(viewport.work_pos)
    imgui.set_next_window_size(viewport.work_size)

    imgui.push_style_var(StyleVar.window_border_size, 0)
    imgui.push_style_var(StyleVar.window_rounding, 0)
    result = begin(label=label, closable=closable, flags=flags)
    imgui.pop_style_var(2)

    try:
        yield result
    finally:
        end()
