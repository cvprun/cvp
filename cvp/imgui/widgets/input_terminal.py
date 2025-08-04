# -*- coding: utf-8 -*-

from typing import Sequence

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.values.delta import DeltaValue


class InputTerminal:
    def __init__(
        self,
        label: str,
        *,
        readonly=False,
        autoscroll=False,
        show_lineno=False,
        show_whitespace=False,
    ):
        self._label = label
        self._readonly = readonly
        self._autoscroll = autoscroll
        self._show_lineno = show_lineno
        self._show_whitespace = show_whitespace
        self._mouse_wheel = DeltaValue.from_single_value(0.0)

    @property
    def autoscroll(self) -> bool:
        return self._autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self._autoscroll = value

    def do_process(self, lines: Sequence[str]) -> None:
        with begin_child_context(self._label):
            if imgui.is_window_hovered(ROOT_AND_CHILD_WINDOWS):
                if self._mouse_wheel.update(imgui.get_io().mouse_wheel):
                    if 0 < self._mouse_wheel.value:
                        # Drag Up
                        if imgui.get_scroll_y() < imgui.get_scroll_max_y():
                            self._autoscroll = False
                    elif self._mouse_wheel.value < 0:
                        # Drag Down
                        if imgui.get_scroll_max_y() <= imgui.get_scroll_y():
                            self._autoscroll = True
                    else:
                        assert 0 == self._mouse_wheel.value

            clipper = imgui.ListClipper()
            clipper.begin(len(lines))
            while clipper.step():
                for i in range(clipper.display_start, clipper.display_end):
                    self.do_line_process(lines, i)

            if self._autoscroll:
                imgui.set_scroll_here_y(1.0)

    def do_line_process(self, lines: Sequence[str], index: int) -> None:
        line_text = lines[index]
        if self._show_lineno:
            lineno_width = len(str(len(lines)))
            imgui.text(f"{index+1:0{lineno_width}}")
            imgui.same_line()

        imgui.text(line_text)
