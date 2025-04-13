# -*- coding: utf-8 -*-

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
from cvp.variables import SIDE_MENU_WIDTH


class DtypePreference(BasePreference):
    __cvp_menu_name__ = "Dtype"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def dtypes(self):
        return self.context.fm.dtypes

    __submenu_dtype_key__ = "dtype"

    @property
    def selected_submenu_dtype(self) -> str:
        return self.get_selected_submenu(self.__submenu_dtype_key__)

    @selected_submenu_dtype.setter
    def selected_submenu_dtype(self, value: str) -> None:
        self.set_selected_submenu(self.__submenu_dtype_key__, value)

    @override
    def do_process(self) -> None:
        child_flags = RESIZE_X | BORDERS
        with begin_child_context("Menu", SIDE_MENU_WIDTH, child_flags=child_flags):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for path, dtype in self.dtypes.items():
                        label = f"{dtype.class_name}###{path}"
                        selected = path == self.selected_submenu_dtype
                        if imgui.selectable(label, selected)[1]:
                            self.selected_submenu_dtype = path
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if dtype := self.dtypes.get(self.selected_submenu_dtype):
                self.do_dtype_process(dtype)
            else:
                text_centered("Please select a item")

    @staticmethod
    def do_dtype_process(dtype: Dtype) -> None:
        input_text_disabled("Class Name", dtype.class_name)
        input_text_disabled("Path", dtype.path)
