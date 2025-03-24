# -*- coding: utf-8 -*-

from imgui_bundle import imgui

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
from cvp.imgui.flags.child import BORDERS
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.tab import TabItem


class RunTab(TabItem[FlowCanvasTabs]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Run")

    @override
    def on_item(self, item: FlowCanvasTabs) -> None:
        opened = item.opened
        opened = False  # TODO: Remove
        button(f"{PLAY} Run", disabled=not opened)

        imgui.same_line()
        button(f"{BUG} Debug", disabled=not opened)

        imgui.same_line()
        button(f"{PAUSE} Pause", disabled=not opened)

        imgui.same_line()
        button(f"{STOP} Stop", disabled=not opened)

        imgui.same_line()
        button(f"{DEBUG_STEP_OVER} Step Over", disabled=not opened)

        imgui.same_line()
        button(f"{DEBUG_STEP_INTO} Step Into", disabled=not opened)

        imgui.same_line()
        button(f"{DEBUG_STEP_OUT} Step Out", disabled=not opened)

        imgui.separator()
        bottom_spacing = imgui.get_style().item_spacing.y
        if begin_child("##Logging", 0, -bottom_spacing, BORDERS):
            pass
