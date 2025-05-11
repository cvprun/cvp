# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.config.sections.navigation import RecentItem
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_WIDTH
from cvp.imgui.flags.child import AUTO_RESIZE_X, AUTO_RESIZE_Y, BORDERS
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.types.override import override


class IntroFlowWindow(BaseWindow):
    __cvp_window_name__ = "Intro"
    __cvp_window_position__ = DockPosition.center_top

    _RECENT_ITEM_SPLIT_X: Final[float] = FIT_WIDTH
    _RECENT_ITEM_CHILD_FLAGS: Final[int] = AUTO_RESIZE_Y | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    @override
    def do_main_process(self) -> None:
        if imgui.button("Open workspace"):
            # self.context.flows.create_new_workspace()
            pass

        imgui.separator()

        imgui.text("Recent workspace")
        # for recent in self.context.get_flow_workspace_recent_items():
        #     self.do_recent_process(recent, i)

    def do_recent_process(self, recent: RecentItem, index: int) -> None:
        with begin_child_context(
            f"Recent {index}",
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
                    pass
            finally:
                imgui.end_horizontal()
