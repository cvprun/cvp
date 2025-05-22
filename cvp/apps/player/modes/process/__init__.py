# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import MONITOR_EYE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class ProcessManagerMode(BaseMode):
    __cvp_mode_name__ = "Process Manager"
    __cvp_mode_icon__ = MONITOR_EYE

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove process?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all process?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

    @property
    def config(self):
        return self.context.config.process

    @property
    def processes(self):
        return self.context.processes

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        assert self

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                with begin_child_context(
                    label="Menu",
                    size=(self._MENU_SPLIT_X, 0),
                    child_flags=self._MENU_CHILD_FLAGS,
                ):
                    self.do_menu_process()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_process := self.processes.get(self.selected_submenu):
                self.do_main_process(selected_process)
            else:
                text_centered("Please select a item")

    def do_menu_process(self) -> None:
        # Table
        pass

    def do_main_process(self, process) -> None:
        # Tab
        pass
