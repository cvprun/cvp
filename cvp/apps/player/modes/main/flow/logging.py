# -*- coding: utf-8 -*-

from logging import CRITICAL, DEBUG, ERROR, INFO, NOTSET, WARNING, Handler, LogRecord
from typing import Callable, Deque, NamedTuple
from weakref import finalize

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.checkbox import checkbox
from cvp.imgui.combo import combo
from cvp.imgui.flags import color_var
from cvp.imgui.flags.child import AUTO_RESIZE_Y
from cvp.imgui.flags.hovered import ROOT_AND_CHILD_WINDOWS
from cvp.imgui.text_colored import text_colored
from cvp.logging.logging import (
    LEVEL_NAMES,
    SEVERITY_NAME_CRITICAL,
    convert_level_number,
)
from cvp.logging.logging import flow_logger as logger
from cvp.patterns.delta import Delta
from cvp.types.colors import RGBA
from cvp.types.override import override


class _LoggingHandler(Handler):
    def __init__(self, callback: Callable[[LogRecord, str], None]):
        super().__init__()
        self._callback = callback

    @override
    def emit(self, record: LogRecord):
        self._callback(record, self.format(record))


class _LineRecord(NamedTuple):
    level: int
    levelname: str
    message: str


def _unregister_handler(handler: _LoggingHandler) -> None:
    logger.removeHandler(handler)


class LoggingFlowWindow(BaseWindow):
    __cvp_window_name__ = "Logging"

    def __init__(self, context: Context):
        super().__init__(context)
        assert 1 <= self.context.config.flow.logs.lines
        self._mouse_wheel = Delta.from_single_value(0.0)
        maxlen = self.context.config.flow.logs.lines
        self._records = Deque[_LineRecord](maxlen=maxlen)
        self._handler = _LoggingHandler(self.on_logging)
        logger.addHandler(self._handler)
        self._finalizer = finalize(self, _unregister_handler, self._handler)

    @property
    def filter(self) -> str:
        return self.context.config.flow.logs.filter

    @filter.setter
    def filter(self, value: str) -> None:
        self.context.config.flow.logs.filter = value

    @property
    def autoscroll(self) -> bool:
        return self.context.config.flow.logs.autoscroll

    @autoscroll.setter
    def autoscroll(self, value: bool) -> None:
        self.context.config.flow.logs.autoscroll = value

    @property
    def lines(self) -> int:
        return self.context.config.flow.logs.lines

    @lines.setter
    def lines(self, value: int) -> None:
        self.context.config.flow.logs.lines = value

    @property
    def level_index(self) -> int:
        return self.context.config.flow.logs.level_index

    @level_index.setter
    def level_index(self, value: int) -> None:
        self.context.config.flow.logs.level_index = value

    def get_level_number(self) -> int:
        return convert_level_number(LEVEL_NAMES[self.level_index])

    def get_level_color(self, level: int) -> RGBA:
        logging_config = self.context.config.flow.logs
        if ERROR < level <= CRITICAL:
            return logging_config.critical_color
        elif WARNING < level <= ERROR:
            return logging_config.error_color
        elif INFO < level <= WARNING:
            return logging_config.warning_color
        elif DEBUG < level <= INFO:
            return logging_config.info_color
        elif NOTSET < level <= DEBUG:
            return logging_config.debug_color
        else:
            vec4 = imgui.get_style().color_(color_var.TEXT)
            return vec4.x, vec4.y, vec4.z, vec4.w

    def on_logging(self, record: LogRecord, message: str) -> None:
        self._records.append(_LineRecord(record.levelno, record.levelname, message))

    def update_records_maxlen(self, maxlen: int) -> None:
        new_lines = type(self._records)(maxlen=maxlen)
        new_lines.extend(self._records)
        self._records = new_lines

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            with begin_child_context("Toolbar", child_flags=AUTO_RESIZE_Y):
                self.do_toolbar_process()
            imgui.separator()
            with begin_child_context("Logging"):
                self.do_logging_process()

    def do_toolbar_process(self) -> None:
        if self._records.maxlen != self.lines:
            self.update_records_maxlen(self.lines)

        self.autoscroll = checkbox("Autoscroll", self.autoscroll)[1]

        imgui.same_line()
        max_width = imgui.calc_text_size(SEVERITY_NAME_CRITICAL)[0]
        padding = imgui.get_style().item_spacing[0] * 2
        dropdown_width = 20.0
        imgui.set_next_item_width(max_width + dropdown_width + padding)
        if level_result := combo("##Levels", self.level_index, LEVEL_NAMES):
            self.level_index = level_result.value

        imgui.same_line()
        imgui.set_next_item_width(-1)
        self.filter = imgui.input_text_with_hint("##Filter", "Filter", self.filter)[1]

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

        filter_level = self.get_level_number()

        for line in self._records:
            if line.level < filter_level:
                continue
            if line.message.find(self.filter) == -1:
                continue

            color = self.get_level_color(line.level)
            text_colored(f"[{line.levelname}] {line.message}", color)

        if self.autoscroll:
            imgui.set_scroll_here_y(1.0)
