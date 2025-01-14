# -*- coding: utf-8 -*-

import imgui

from cvp.context.context import Context
from cvp.fonts.glyphs.mdi import (
    BUG,
    DEBUG_STEP_INTO,
    DEBUG_STEP_OUT,
    DEBUG_STEP_OVER,
    PAUSE,
    PLAY,
    STOP,
)
from cvp.imgui.begin_child import begin_child
from cvp.imgui.button import button
from cvp.imgui.fonts.mapper import FontMapper
from cvp.types.override import override
from cvp.widgets.tab import TabItem
from cvp.windows.flow.canvases import Canvases


class RunTab(TabItem[Canvases]):
    def __init__(self, context: Context, fonts: FontMapper):
        super().__init__(context, "Run")
        self._fonts = fonts

    @override
    def on_item(self, item: Canvases) -> None:
        opened = item.opened
        if self._fonts.normal_icon:
            button(f"{PLAY} Run", disabled=not opened)

        imgui.same_line()
        if self._fonts.normal_icon:
            button(f"{BUG} Debug", disabled=not opened)

        imgui.same_line()
        if self._fonts.normal_icon:
            button(f"{PAUSE} Pause", disabled=not opened)

        imgui.same_line()
        if self._fonts.normal_icon:
            button(f"{STOP} Stop", disabled=not opened)

        imgui.same_line()
        if self._fonts.normal_icon:
            button(f"{DEBUG_STEP_OVER} Step Over", disabled=not opened)

        imgui.same_line()
        if self._fonts.normal_icon:
            button(f"{DEBUG_STEP_INTO} Step Into", disabled=not opened)

        imgui.same_line()
        if self._fonts.normal_icon:
            button(f"{DEBUG_STEP_OUT} Step Out", disabled=not opened)

        imgui.separator()
        bottom_spacing = imgui.get_style().item_spacing.y
        with begin_child("##Logging", 0, -bottom_spacing, border=False):
            pass
