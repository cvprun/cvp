# -*- coding: utf-8 -*-

from typing import Final, Optional, Union

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FILE_LOCK
from cvp.context.context import Context
from cvp.hashfunc.checksum import HashFunction, checksum
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import READ_ONLY
from cvp.imgui.input_text_multilingual import input_text_multiline
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class HashMode(BaseMode):
    __cvp_mode_name__ = "Hash Functions"
    __cvp_mode_icon__ = FILE_LOCK

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)
        self._methods = [str(m) for m in HashFunction]
        self._input = str()
        self._output = str()
        self._error: Optional[Union[BaseException, str]] = None
        self._encoding = "utf-8"
        self._errors = "strict"

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def get_selected_method(
        self,
        method_name: Optional[str] = None,
    ) -> Optional[HashFunction]:
        if not method_name:
            method_name = self.selected_submenu
        assert isinstance(method_name, str)

        try:
            index = self._methods.index(method_name)
            return HashFunction(self._methods[index])
        except ValueError:
            return None

    def update_encode(self, method: HashFunction, value: str) -> None:
        self._input = value

        if not self._input:
            self._output = str()
            self._error = None
            return

        try:
            data = self._input.encode(encoding=self._encoding, errors=self._errors)
            self._output = checksum(method, data)
            print(f"Output: {method} {data!r} -> {self._output}")
            self._error = None
        except BaseException as e:
            self._output = str()
            self._error = e if str(e) else type(e).__name__

    def clear_fields(self) -> None:
        self._input = str()
        self._output = str()
        self._error = None

    @staticmethod
    def convert_displayable_text(method_name: str) -> str:
        return method_name.upper().replace("_", "-")

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for method_name in self._methods:
                        display = self.convert_displayable_text(method_name)
                        label = f"{display}##{method_name}"
                        selected = method_name == self.selected_submenu
                        if imgui.selectable(label, selected)[1]:
                            if self.selected_submenu != method_name:
                                selected_method = self.get_selected_method(method_name)
                                assert selected_method is not None
                                self.update_encode(selected_method, self._input)
                            self.selected_submenu = method_name
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if method := self.get_selected_method():
                self.do_method_process(method)
            else:
                text_centered("Please select a item")

    def do_method_process(self, method: HashFunction) -> None:
        display = self.convert_displayable_text(method)
        imgui.text(f"Hash Function : {display}")
        imgui.same_line()
        if imgui.small_button("Clear"):
            self.clear_fields()
        imgui.separator()

        available_space = imgui.get_content_region_avail()
        item_spacing = imgui.get_style().item_spacing
        total_empty_width = item_spacing.x * 2.0  # center and right padding
        half_width = (available_space.x - total_empty_width) / 2.0

        with begin_child_context("MainLeft", (half_width, 0), RESIZE_X):
            imgui.text("Input")

            if imgui.button("Clipboard"):
                self.update_encode(method, imgui.get_clipboard_text())
            imgui.same_line()
            if imgui.button("Copy"):
                imgui.set_clipboard_text(self._input)

            input_result = input_text_multiline("##Input", self._input, FIT_SIZE)
            if self._input != input_result.value:
                self.update_encode(method, input_result.value)

        imgui.same_line()

        with begin_child_context("MainBottom"):
            imgui.text("Output")

            if imgui.button("Copy"):
                imgui.set_clipboard_text(self._output)

            if self._error is not None:
                imgui.text_colored(self.error_color, str(self._error))
            else:
                input_text_multiline("##Output", self._output, FIT_SIZE, READ_ONLY)
