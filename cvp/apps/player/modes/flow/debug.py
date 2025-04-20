# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
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
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.types.override import override


class DebugFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Debug"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            self.do_child_process()

    @staticmethod
    def do_child_process() -> None:
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
        with begin_child_context("Logging"):
            pass
