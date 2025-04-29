# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.config.sections.navigation import RecentItem
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.child import AUTO_RESIZE_X, AUTO_RESIZE_Y, BORDERS
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.types.override import override


class IntroFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Intro"

    _RECENT_ITEM_SPLIT_X: Final[float] = FIT_WIDTH
    _RECENT_ITEM_CHILD_FLAGS: Final[int] = AUTO_RESIZE_Y | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.flow

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            if imgui.button("Open workspace"):
                # self.context.flows.create_new_workspace()
                pass

            imgui.separator()

            imgui.text("Recent workspace")
            for recent in self.context.get_flow_workspace_recent_items():
                self.do_recent_process(recent)

    def do_recent_process(self, recent: RecentItem) -> None:
        with begin_child_context(
            f"Recent##{recent.value}",
            size=(self._RECENT_ITEM_SPLIT_X, 0),
            child_flags=self._RECENT_ITEM_CHILD_FLAGS,
        ):
            with begin_child_context("Left", child_flags=AUTO_RESIZE_X | AUTO_RESIZE_Y):
                imgui.text(recent.value)

                with style_disable_input_context():
                    imgui.text(recent.accessed_at)

            imgui.same_line()

            avail_size = imgui.get_content_region_avail()
            imgui.begin_horizontal("Horizontal", size=(avail_size.x, 0))
            try:
                imgui.spring()
                if imgui.button("Open", size=(0, avail_size.y)):
                    self.context.open_flow_workspace(recent.value)
            finally:
                imgui.end_horizontal()
