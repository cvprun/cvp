# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.dtypes.dtype import Dtype
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class DtypePreference(BasePreference):
    __cvp_menu_name__ = "Dtype"

    _MENU_SPLIT_X: Final[int] = 150
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def dtypes(self):
        return self.context.flows.dtypes

    @override
    def do_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for path, dtype in self.dtypes.items():
                        label = f"{dtype.class_name}###{path}"
                        selected = path == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = path
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if dtype := self.dtypes.get(self.selected):
                self.do_dtype_process(dtype)
            else:
                text_centered("Please select a item")

    @staticmethod
    def do_dtype_process(dtype: Dtype) -> None:
        input_text_disabled("Class Name", dtype.class_name)
        input_text_disabled("Path", dtype.path)
