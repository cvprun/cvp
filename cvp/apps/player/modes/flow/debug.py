# -*- coding: utf-8 -*-

from typing import Optional

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.apps.player.windows.graph import FlowGraphWindow
from cvp.assets.fonts import mdi
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class DebugFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Debug"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self, window: Optional[FlowGraphWindow]) -> None:
        with begin_context(self.get_window_name()):
            with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
                self.do_toolbar_process()
            imgui.separator()
            with begin_child_context("Logging"):
                if window is not None:
                    self.do_logging_process()
                else:
                    text_centered("Please select a graph")

    @staticmethod
    def do_toolbar_process() -> None:
        opened = False  # TODO: Remove
        button(f"{mdi.PLAY} Run", disabled=not opened)

        imgui.same_line()
        button(f"{mdi.BUG} Debug", disabled=not opened)

        imgui.same_line()
        button(f"{mdi.PAUSE} Pause", disabled=not opened)

        imgui.same_line()
        button(f"{mdi.STOP} Stop", disabled=not opened)

        imgui.same_line()
        button(f"{mdi.DEBUG_STEP_OVER} Step Over", disabled=not opened)

        imgui.same_line()
        button(f"{mdi.DEBUG_STEP_INTO} Step Into", disabled=not opened)

        imgui.same_line()
        button(f"{mdi.DEBUG_STEP_OUT} Step Out", disabled=not opened)

    @staticmethod
    def do_logging_process() -> None:
        pass
