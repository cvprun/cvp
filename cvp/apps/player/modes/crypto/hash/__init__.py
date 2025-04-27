# -*- coding: utf-8 -*-

from typing import Final, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.hashfunc.checksum import Method
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class HashMode(BaseMode):
    __cvp_mode_name__ = "Hash Functions"

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._methods = [str(m) for m in Method]

    @override
    def do_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def get_selected_method(self) -> Optional[Method]:
        try:
            index = self._methods.index(self.selected_submenu)
            return Method(self._methods[index])
        except ValueError:
            return None

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for method_name in self._methods:
                        selected = method_name == self.selected_submenu
                        if imgui.selectable(method_name, selected)[1]:
                            self.selected_submenu = method_name
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if method := self.get_selected_method():
                self.do_method_process(method)
            else:
                text_centered("Please select a item")

    def do_method_process(self, method: Method) -> None:
        pass
