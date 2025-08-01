# -*- coding: utf-8 -*-

from typing import Iterable

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.values.delta import DeltaValue


class TerminalCanvas:
    def __init__(self, label: str, autoscroll=True):
        self._label = label
        self._autoscroll = autoscroll
        self._mouse_wheel = DeltaValue.from_single_value(0.0)

    @property
    def autoscroll(self) -> bool:
        return self._autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self._autoscroll = value

    def do_process(self, lines: Iterable[str]) -> None:
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

            for line in lines:
                imgui.text(line)

            if self._autoscroll:
                imgui.set_scroll_here_y(1.0)
