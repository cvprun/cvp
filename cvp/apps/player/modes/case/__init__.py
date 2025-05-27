# -*- coding: utf-8 -*-

from io import StringIO
from typing import Final, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FORMAT_LETTER_CASE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import READ_ONLY
from cvp.imgui.input_text_multiline import input_text_multiline
from cvp.imgui.text_centered import text_centered
from cvp.strings.case_converter import CaseType, convert_case
from cvp.types.override import override
from cvp.variables import NEWLINE


class CaseMode(BaseMode):
    __cvp_mode_name__ = "Case Converter"
    __cvp_mode_icon__ = FORMAT_LETTER_CASE

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _DEMO_TEXT: Final[str] = (
        "helloWorld\n"
        "HelloWorld\n"
        "hello_world\n"
        "HELLO_WORLD\n"
        "hello-world\n"
        "Hello-World\n"
        "hello world\n"
        "Hello World\n"
        "Hello world\n"
        "hello.world\n"
    )

    def __init__(self, context: Context):
        super().__init__(context)
        self._types = [str(m) for m in CaseType]
        self._input = str()
        self._output = str()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def get_selected_type(self, case_type: Optional[str] = None) -> Optional[CaseType]:
        if not case_type:
            case_type = self.selected_submenu
        assert isinstance(case_type, str)

        try:
            index = self._types.index(case_type)
            return CaseType(self._types[index])
        except ValueError:
            return None

    def do_convert_case(self, method: CaseType, value: str) -> None:
        self._input = value

        if not self._input:
            self._output = str()
            return

        buffer = StringIO()
        for line in self._input.split(NEWLINE):
            buffer.write(convert_case(method, line))
            buffer.write(NEWLINE)

        self._output = buffer.getvalue()

    def clear_fields(self) -> None:
        self._input = str()
        self._output = str()

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for case_name in self._types:
                        selected = case_name == self.selected_submenu
                        if imgui.selectable(case_name, selected)[1]:
                            if self.selected_submenu != case_name:
                                selected_method = self.get_selected_type(case_name)
                                assert selected_method is not None
                                self.do_convert_case(selected_method, self._input)
                            self.selected_submenu = case_name
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if case_type := self.get_selected_type():
                self.do_method_process(case_type)
            else:
                text_centered("Please select a item")

    def do_method_process(self, case_type: CaseType) -> None:
        imgui.text(f"Case Type : {case_type}")
        imgui.separator()

        available_space = imgui.get_content_region_avail()
        item_spacing = imgui.get_style().item_spacing
        total_empty_width = item_spacing.x * 2.0  # center and right padding
        half_width = (available_space.x - total_empty_width) / 2.0

        with begin_child_context("MainLeft", (half_width, 0), RESIZE_X):
            imgui.text("Input")

            if imgui.button("Demo"):
                self.do_convert_case(case_type, self._DEMO_TEXT)
            imgui.same_line()
            if imgui.button("Clipboard"):
                self.do_convert_case(case_type, imgui.get_clipboard_text())
            imgui.same_line()
            if imgui.button("Copy"):
                imgui.set_clipboard_text(self._input)
            imgui.same_line()
            if imgui.small_button("Clear"):
                self.clear_fields()

            input_result = input_text_multiline("##Input", self._input, FIT_SIZE)
            if self._input != input_result.value:
                self.do_convert_case(case_type, input_result.value)

        imgui.same_line()

        with begin_child_context("MainBottom"):
            imgui.text("Output")

            if imgui.button("Copy"):
                imgui.set_clipboard_text(self._output)

            input_text_multiline("##Output", self._output, FIT_SIZE, READ_ONLY)
