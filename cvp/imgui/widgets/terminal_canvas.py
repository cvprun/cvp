# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Deque, Dict, Iterable, Optional

from imgui_bundle import imgui

from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.patterns.singleton import singleton
from cvp.values.delta import DeltaValue
from cvp.variables import INFINITE


@dataclass
class TerminalCanvasOptions:
    lines: int = INFINITE
    autoscroll: bool = True

    @property
    def maxlen(self) -> Optional[int]:
        if self.lines == INFINITE:
            return None
        else:
            return self.lines


class TerminalCanvas:
    def __init__(
        self,
        label: str,
        lines: Optional[Iterable[str]] = None,
        options: Optional[TerminalCanvasOptions] = None,
    ):
        self._label = label
        self._options = options if options else TerminalCanvasOptions()
        self._mouse_wheel = DeltaValue.from_single_value(0.0)
        self._lines = self._create_lines(lines, self._options.maxlen)

    @staticmethod
    def _create_lines(
        iterable: Optional[Iterable[str]] = None,
        maxlen: Optional[int] = None,
    ):
        if iterable:
            return Deque[str](iterable, maxlen=maxlen)
        else:
            return Deque[str](maxlen=maxlen)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value: TerminalCanvasOptions) -> None:
        self._options = value

    @property
    def autoscroll(self) -> bool:
        return self._options.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self._options.autoscroll = value

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value: Deque[str]) -> None:
        self._lines = value

    def do_process(self) -> None:
        with begin_child_context(type(self).__name__):
            self.do_update_buffer()
            self.do_logging_process()

    def do_update_buffer(self) -> None:
        if self._lines.maxlen == self._options.maxlen:
            return

        old_lines = list(self._lines)
        self._lines = self._create_lines(old_lines, self._options.maxlen)

    def do_logging_process(self) -> None:
        if imgui.is_window_hovered(ROOT_AND_CHILD_WINDOWS):
            if self._mouse_wheel.update(imgui.get_io().mouse_wheel):
                if 0 < self._mouse_wheel.value:
                    # Drag Up
                    if imgui.get_scroll_y() < imgui.get_scroll_max_y():
                        self.autoscroll = False
                elif self._mouse_wheel.value < 0:
                    # Drag Down
                    if imgui.get_scroll_max_y() <= imgui.get_scroll_y():
                        self.autoscroll = True
                else:
                    assert 0 == self._mouse_wheel.value

        for line in self._lines:
            imgui.text(line)

        if self.autoscroll:
            imgui.set_scroll_here_y(1.0)


@singleton
class GlobalTerminalCanvasOptions(Dict[int, TerminalCanvasOptions]):
    pass


def terminal_canvas(
    label: str,
    lines: Optional[Iterable[str]] = None,
    options: Optional[TerminalCanvasOptions] = None,
):
    if options is None:
        global_options = GlobalTerminalCanvasOptions()
        next_id = imgui.get_id(label)
        options = global_options.get(next_id)
        if options is None:
            options = TerminalCanvasOptions()
            global_options.__setitem__(next_id, options)

    table = TerminalCanvas(label, lines, options)
    return table.do_process()
